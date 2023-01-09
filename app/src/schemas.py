from pydantic import BaseModel


class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_pic_url: str | None = None


class LoggedInUser(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
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


class LinkTokenForUser(BaseModel):
    link_token: str
    user_id: str
