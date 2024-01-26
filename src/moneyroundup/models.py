from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from moneyroundup.database import Base


class UserOld(Base):
    __tablename__ = "old_users"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    profile_pic_url = Column(String)
    items = relationship("Item")

    def __str__(self) -> str:
        return f"User<{self.first_name} | {self.last_name} | {self.email} | {self.id}>"


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True)
    user_id = Column(ForeignKey("old_users.id"))
    access_token = Column(String)
    active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return f"Item<{self.id}> | | {self.access_token} | {self.active}>"


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column("user_id", String, ForeignKey("user.id"))
    goal: Mapped[dict] = mapped_column("goal", JSONB, nullable=True)