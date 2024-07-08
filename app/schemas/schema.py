from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    email: str
    disabled: bool = False

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class ListingBase(BaseModel):
    id_user: int
    name: str
    photo: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    description: str

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    street: str
    zipcode: str
    city: str
    latitude: float
    longitude: float
    listing_id: int

    class Config:
        orm_mode = True


class ProposalBase(BaseModel):
    id_listing: int
    proposer_id: int
    proposal_msg: str

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    proposal_id: int

    class Config:
        orm_mode = True


class ConversationMessageBaseModel(BaseModel):
    conversation_id: int
    sender_id: int
    message: str

    class Config:
        orm_mode = True
