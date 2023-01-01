from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from typing import Optional
from base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    first_name: Mapped[str] = Column(String(50))
    last_name: Column = Column(String(50))
    email: Mapped[str] = Column(String(100), unique=True, index=True)
    profile_pic_url: Mapped[str] = Column(String)
    items = relationship("Item")

    def __str__(self) -> str:
        return f"User<{self.first_name} | {self.last_name} | {self.email} | {self.id}>"

class Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = Column(String, primary_key=True)
    user_id: Mapped[str] = Column(ForeignKey("users.id"))
    access_token: Mapped[str] = Column(String)
    active: Mapped[bool] = Column(Boolean, default=True)

    def __str__(self) -> str:
        return f"Item<{self.id}> | {self.user_id} | {self.access_token} | {self.active}>"