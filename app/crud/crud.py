from sqlalchemy.orm import Session
from app.models.models import *

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


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
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


def get_listings_by_user_id(db: Session, user_id: int):
    return db.query(Listing).filter(Listing.id_user == user_id).all()


def create_listings(db: Session, listing: Listing):
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

# PROPOSAL CRUD


def get_proposal_created(db, listing_id):
    return db.query(Proposal).filter(Proposal.id_listing == listing_id).first()


def create_proposal(db: Session, proposal: Proposal):
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal

# CONVERSATION CRUD


def create_conversation(db: Session, conversation: Conversation):
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

# MESSAGE CRUD


def create_message(db: Session, message: ConversationMessage):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_by_conversation_id(db: Session, conversation_id: int):
    return db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conversation_id).all()


# PLANTE CRUD
def get_all_plantes(db: Session):
    return db.query(Plante).all()


def create_plantes(db: Session, plantes: Plante):
    db.add(plantes)
    db.commit()
    db.refresh(plantes)
    return plantes


# POST CRUD
def create_post(db: Session, post: Post):
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts_by_plante_id(db: Session, plante_id: int):
    return db.query(Post).filter(Post.plante_id == plante_id).all()
