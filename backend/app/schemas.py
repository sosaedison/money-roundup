from pydantic import BaseModel

class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_pic_url: str | None = None

class PublicTokenExchangeBody(BaseModel):
    public_token: str
    metadata: object
    user_id: str
