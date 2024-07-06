from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routes.route import router
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuring CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
SQLModel.metadata.create_all(engine)

app.include_router(router)
