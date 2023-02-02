from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from moneyroundup.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    profile_pic_url = Column(String)
    items = relationship("Item")

    def __str__(self) -> str:
        return f"User<{self.first_name} | {self.last_name} | {self.email} | {self.id}>"


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    access_token = Column(String)
    active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return (
            f"Item<{self.id}> | {self.user_id} | {self.access_token} | {self.active}>"
        )
