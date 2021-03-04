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
    book_cover = open("app/tests/book_cover.jpg", "rb")
    res = client.post(
        Books.create,
        headers={'Authorization': f'Bearer {access_token}'},
        files={"cover": book_cover},
        data={
            "name": "Fahrenheit 451",
            "author": "Ray Bradbury"
        }
    )
    assert res.status_code == 200
