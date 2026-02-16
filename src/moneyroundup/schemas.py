from pydantic import BaseModel


class PublicTokenExchangeBody(BaseModel):
    public_token: str


class CreateNewItem(BaseModel):
    access_token: str


class NewItemCreated(BaseModel):
    item_created: bool
