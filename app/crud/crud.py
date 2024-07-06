from sqlalchemy import func
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


def delete_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    db.delete(user)
    db.commit()
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
    current_time = datetime.datetime.utcnow()
    return db.query(Listing).filter(Listing.end_date >= current_time).all()


def get_listings_by_id(db: Session, id: int):
    return db.query(Listing).filter(Listing.id == id).first()


def get_listings_by_user_id(db: Session, user_id: int):
    reponse = db.query(Listing).filter(Listing.id_user == user_id).all()
    reponse += db.query(Listing).join(Proposal, Listing.id ==
                                      Proposal.id_listing).filter(Proposal.proposer_id == user_id).all()
    return reponse


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


def get_all_last_message_of_conversation_by_user_id(db: Session, user_id: int):
    # Subquery to find the latest timestamp for each conversation
    subquery = db.query(
        ConversationMessage.conversation_id,
        func.max(ConversationMessage.timestamp).label('max_timestamp')
    ).group_by(ConversationMessage.conversation_id).subquery()

    # Join the subquery to get the most recent message of each conversation
    # Adjust the filter condition if you need to consider messages received by the user as well
    # Order by timestamp in descending order to get the most recent messages first
    return db.query(ConversationMessage).join(
        subquery,
        (ConversationMessage.conversation_id == subquery.c.conversation_id) &
        (ConversationMessage.timestamp == subquery.c.max_timestamp)
    ).filter(ConversationMessage.sender_id == user_id).order_by(ConversationMessage.timestamp.desc()).all()

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
