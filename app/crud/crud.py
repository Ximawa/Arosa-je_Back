from sqlalchemy.orm import Session
from models.models import *

# USER CRUD


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()
# ROLE CRUD


def get_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_title(db: Session, role_title: str):
    return db.query(Role).filter(Role.title == role_title).first()


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

# LISTING CRUD


def get_listings(db: Session):
    return db.query(Listing).all()


def get_listings_by_id(db: Session, id: int):
    return db.query(Listing).filter(Listing.id == id).first()


def create_listings(db: Session, listing: Listing):
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing
