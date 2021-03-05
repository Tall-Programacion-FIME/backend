import time
import uuid

from fastapi.testclient import TestClient

from .urls import *
from ..main import app

client = TestClient(app)

name = "Sebastian Marines"
email = uuid.uuid4().hex + "testingadmin@uanl.edu.mx"
password = "admin"
user_id = None
access_token = None
refresh_token = None
book_id = None


def test_create_user():
    """Tests register function"""
    global user_id
    res = client.post(Users.user, json={
        "email": email,
        "name": name,
        "password": password
    })
    json_response = res.json()
    assert res.status_code == 200
    assert json_response["email"] == email
    assert json_response["is_active"] is True
    user_id = json_response["id"]


def test_already_registered_email():
    res = client.post(Users.user, json={
        "email": email,
        "name": name,
        "password": password
    })
    assert res.status_code == 400


def test_get_user_by_id():
    res = client.get(f"{Users.user}{user_id}")
    assert res.status_code == 200
    assert "email" in res.text


def test_non_existing_id():
    res = client.get(f"{Users.user}1000000")
    assert res.status_code == 404


def test_login_for_access_token():
    global access_token
    global refresh_token
    res = client.post(Auth.login, json={
        "email": email,
        "password": password
    })
    json_res = res.json()
    assert res.status_code == 200
    access_token = json_res["access_token"]
    refresh_token = json_res["refresh_token"]
    assert access_token is not None


def test_login_with_incorrect_email():
    res = client.post(Auth.login, json={
        "email": "nonexisting@admin.com",
        "password": "admin"
    })
    assert res.status_code == 401


def test_login_with_incorrect_password():
    res = client.post(Auth.login, json={
        "email": email,
        "password": "notmypassword"
    })
    assert res.status_code == 401


def test_user_page():
    res = client.get(Users.profile, headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert res.status_code == 200
    assert res.json() == {
        'email': email,
        'name': name,
        'id': user_id,
        'books_for_sale': [],
        'is_active': True
    }


def test_valid_email():
    """Tests that only school emails can register"""
    res = client.post(Users.user, json={
        "email": "admin@otherdomain.com",
        "name": name,
        "password": "admin"
    })
    assert res.status_code == 403


def test_token_refresh():
    res = client.post(Auth.refresh_token, headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    assert "access_token" in res.text
    assert "refresh_token" not in res.text


def test_upload_book():
    global book_id
    book_cover = open("app/tests/book_cover.jpg", "rb")
    res = client.post(
        Books.create,
        headers={'Authorization': f'Bearer {access_token}'},
        files={"cover": book_cover},
        data={
            "name": "Fahrenheit 451",
            "author": "Ray Bradbury",
            "price": 100
        }
    )
    book_id = res.json()["id"]
    assert res.status_code == 200


def test_upload_book_with_unsupported_file_type():
    book_cover = open("app/tests/dummy.pdf", "rb")
    res = client.post(
        Books.create,
        headers={'Authorization': f'Bearer {access_token}'},
        files={"cover": book_cover},
        data={
            "name": "Not an image",
            "author": "Not an author",
            "price": 100
        }
    )
    assert res.status_code == 400


def test_get_book():
    res = client.get(Books.base + str(book_id))
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["name"] == "Fahrenheit 451"
    assert res_json["author"] == "Ray Bradbury"
    assert res_json["price"] == 100


def test_non_existent_book():
    res = client.get(Books.base + "100000")
    assert res.status_code == 404


def test_list_books():
    res = client.get(Books.base)
    res_json = res.json()
    assert len(res_json) > 0


def test_search_book():
    time.sleep(1)  # TODO wait for elasticsearch to update document
    res = client.get(Books.search, params={'q': 'Fahrenheit'})
    res_json = res.json()
    assert res.status_code == 200
    assert len(res_json) != 0


def test_not_found_search():
    res = client.get(Books.search, params={'q': 'Edgar Danilo'})
    assert res.status_code == 404


def test_update_book():
    res = client.post(
        Books.base + str(book_id),
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            "name": "Another Book",
            "author": "Another author",
            "price": 500
        }
    )
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["name"] == "Another Book"
    assert res_json["author"] == "Another author"
    assert res_json["price"] == 500
