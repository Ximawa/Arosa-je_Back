from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str
    hashed_password: str
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
    start_date: str
    end_date: str
    description: str


class Proposal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_listing: int = Field(foreign_key="listing.id")
    proposer_id: int = Field(foreign_key="user.id")
    proposal_msg: str
