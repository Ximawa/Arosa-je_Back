from fastapi import FastAPI
from sqlmodel import SQLModel
from routes.route import router
from functions.functions import authenticate_user, create_access_token
from database import engine

app = FastAPI()

# Create tables
SQLModel.metadata.create_all(engine)

app.include_router(router)