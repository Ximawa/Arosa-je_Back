from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timezone, timedelta
from app.crud.crud import get_user_by_username
from app.database import SessionLocal
import bcrypt


def read_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key


# Chemin vers le fichier contenant la clé d'API
file_path = 'app/config.txt'

# Secret key to sign JWT token
SECRET_KEY = read_api_key(file_path)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = get_user_by_username(db, username)
    db.close()
    if not user:
        return False
    stored_hashed_password = user.password.encode('utf-8')
    provided_password = password.encode('utf-8')

    if not bcrypt.checkpw(provided_password, stored_hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token JWT manquant")
