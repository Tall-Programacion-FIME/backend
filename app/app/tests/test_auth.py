import uuid

from fastapi.testclient import TestClient

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
    res = client.post("/user/", json={
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
    res = client.post("/user/", json={
        "email": email,
        "name": name,
        "password": password
    })
    assert res.status_code == 400


def test_get_user_by_id():
    res = client.get(f"/user/{user_id}")
    assert res.status_code == 200
    assert "email" in res.text


def test_non_existing_id():
    res = client.get("/user/1000000")
    assert res.status_code == 404


def test_login_for_access_token():
    global access_token
    global refresh_token
    res = client.post("/token", json={
        "email": email,
        "password": password
    })
    json_res = res.json()
    assert res.status_code == 200
    access_token = json_res["access_token"]
    refresh_token = json_res["refresh_token"]
    assert access_token is not None


def test_login_with_incorrect_email():
    res = client.post("/token", json={
        "email": "nonexisting@admin.com",
        "password": "admin"
    })
    assert res.status_code == 401


def test_login_with_incorrect_password():
    res = client.post("/token", json={
        "email": email,
        "password": "notmypassword"
    })
    assert res.status_code == 401


def test_user_page():
    res = client.get("/user/me", headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert res.status_code == 200
    assert res.json() == {
        'email': email,
        'name': name,
        'id': user_id,
        'is_active': True
    }


def test_valid_email():
    """Tests that only school emails can register"""
    res = client.post("/user/", json={
        "email": "admin@otherdomain.com",
        "name": name,
        "password": "admin"
    })
    assert res.status_code == 403


def test_token_refresh():
    res = client.post("/refresh_token", headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    assert "access_token" in res.text
    assert "refresh_token" not in res.text

