from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


def test_register():
    response = client.post(
        '/register',
        data={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'id_role': 1
        }
    )
    assert response.status_code == 200
    assert response.json()['disabled'] == False
    assert response.json()['username'] == 'testuser'
    assert response.json()['password'] == 'testpassword'
    assert response.json()['email'] == 'test@example.com'
    assert response.json()['full_name'] == 'Test User'
    assert response.json()['id_role'] == 1
    assert isinstance(response.json()['id'], int)


def test_login():
    response = client.post(
        '/login',
        data={
            'grant_type': 'password',
            'username': 'testuser',
            'password': 'testpassword',
            'scope': 'read write'
        }
    )
    assert response.status_code == 200
    assert response.json()['token_type'] == "bearer"
    assert isinstance(response.json()['access_token'], str)


def test_wrong_username():
    response = client.post(
        '/login',
        data={
            'grant_type': 'password',
            'username': 'wronguser',
            'password': 'testpassword',
            'scope': 'read write'
        }
    )
    assert response.status_code == 401
    with pytest.raises(HTTPException):
        if response.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password")


def test_wrong_value():
    response = client.post(
        '/register',
        data={
            'username': None,
            'password': None,
            'email': 'test@example.com',
            'full_name': 'Test User',
            'id_role': '1'
        }
    )
    assert response.status_code == 422
