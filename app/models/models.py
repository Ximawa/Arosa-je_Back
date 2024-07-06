import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str
    password: str
    disabled: bool = False
    id_role: int = Field(foreign_key="role.id")


class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str


class Listing(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_user: int = Field(foreign_key="user.id")
    name: str
    photo: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    description: str


class Address(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    street: str
    zipcode: str
    city: str
    latitude: float
    longitude: float
    listing_id: int = Field(foreign_key="listing.id")


class Proposal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_listing: int = Field(foreign_key="listing.id")
    proposer_id: int = Field(foreign_key="user.id")
    proposal_msg: str


class Conversation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    proposal_id: int = Field(foreign_key="proposal.id")


class ConversationMessageBase(SQLModel):
    conversation_id: int
    sender_id: int
    message: str


class ConversationMessage(ConversationMessageBase, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow)


class ConversationMessageIn(ConversationMessageBase):
    pass


class Plante(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    photo: str
    name: str
    description: str


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    plante_id: int = Field(foreign_key="plante.id")
    user_id: int = Field(foreign_key="user.id")
    content: str
    create_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow)
