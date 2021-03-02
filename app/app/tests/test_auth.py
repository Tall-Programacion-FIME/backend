import random
import string

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def get_random_string(length: int = 5) -> str:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def test_create_user():
    email = get_random_string() + "@uanl.edu.mx"
    password = "admin"
    res = client.post("/user/", json={
        "email": email,
        "password": password
    })
    json_response = res.json()
    assert res.status_code == 200
    assert json_response["email"] == email
    assert json_response["is_active"] is True
