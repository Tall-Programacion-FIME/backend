import random
import string

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_create_user():
    """Tests register function"""
    email = "testingadmin@uanl.edu.mx"
    password = "admin"
    res = client.post("/user/", json={
        "email": email,
        "password": password
    })
    json_response = res.json()
    assert res.status_code == 200
    assert json_response["email"] == email
    assert json_response["is_active"] is True


def test_already_registered_email():
    email = "testingadmin@uanl.edu.mx"
    password = "admin"
    res = client.post("/user/", json={
        "email": email,
        "password": password
    })
    assert res.status_code == 400


def test_get_user_by_id():
    res = client.get("/user/1")
    assert res.status_code == 200
    assert "email" in res.text


def test_valid_email():
    """Tests that only school emails can register"""
    res = client.post("/user/", json={
        "email": "admin@otherdomain.com",
        "password": "admin"
    })
    assert res.status_code == 400
