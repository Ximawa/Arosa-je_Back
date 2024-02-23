from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from functions.functions import *
from crud.crud import *
from database import get_db
from models.models import *

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "login": user.username,
            "id": user.id,
            "role": user.id_role
        }, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def create_new_user(user: User, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return create_user(db, user)


@router.get("/roles")
def get_all_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/CreateRole")
def create_new_role(role: Role, db: Session = Depends(get_db)):
    db_role = get_role_by_title(db, role_title=role.title)
    if db_role:
        raise HTTPException(
            status_code=400, detail="Role already exists")
    return create_role(db, role)


@router.get("/listing")
def get_all_listing(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return get_listings(db)


@router.post("/CreateListing")
def create_new_listing(listing: Listing, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return create_listings(db, listing)
