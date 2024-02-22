from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from crud.crud import get_user, create_user
from database import SessionLocal
from models.models import User

# Secret key to sign JWT token
SECRET_KEY = "c25d69952511253e2cad5ec254751225"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing library for password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO fix password check
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = get_user(db, username)
    db.close()
    if not user:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
