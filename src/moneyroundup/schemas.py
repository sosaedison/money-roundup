import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_pic_url: str | None = None


class UserFromDB(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    profile_pic_url: str | None = None

    class Config:
        from_attributes = True


class LoggedInUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    access_token: str
    profile_pic_url: str | None = None


class PublicTokenExchangeBody(BaseModel):
    public_token: str


class CreateNewItem(BaseModel):
    user_id: str | None = None
    access_token: str


class NewItemCreated(BaseModel):
    item_created: bool


class UserRequestingLinkToken(BaseModel):
    user_id: str
    access_token: str


class LinkTokenForUser(BaseModel):
    link_token: str
    user_id: str
