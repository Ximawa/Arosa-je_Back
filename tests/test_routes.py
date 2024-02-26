from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
import bcrypt
from app.main import app

client = TestClient(app)


def test_register():
    hashed_password = bcrypt.hashpw(b'testpassword', bcrypt.gensalt())
    response = client.post(
        '/register',
        data={
            'username': 'testuser',
            'password': hashed_password.decode('utf-8'),
            'email': 'test@example.com',
            'full_name': 'Test User',
            'id_role': 1
        }
    )
    assert response.status_code == 200
    assert response.json()['disabled'] == False
    assert response.json()['username'] == 'testuser'
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


def test_wrong_password():
    response = client.post(
        '/login',
        data={
            'grant_type': 'password',
            'username': 'testuser',
            'password': 'wrongpassword',
            'scope': 'read write'
        }
    )
    assert response.status_code == 401
    with pytest.raises(HTTPException):
        if response.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password")


def test_empty_value():
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


def test_get_all_roles():
    response = client.get('/roles')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_user():
    # Test case for deleting a user
    response = client.post(
        '/deleteUser',
        data={
            'username': 'testuser'
        }
    )
    assert response.status_code == 200
