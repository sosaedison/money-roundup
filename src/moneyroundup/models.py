from uuid import uuid4

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import JSON, UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from moneyroundup.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    # oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
    #     "OAuthAccount", lazy="joined"
    # )
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    def __str__(self) -> str:
        return f"USER({self.first_name} | {self.email} | {self.is_active})"

class Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    access_token: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)

    def __str__(self) -> str:
        return f"Item<{self.id}> | | {self.access_token} | {self.active}>"


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"))
    goal: Mapped[dict] = mapped_column(JSON, nullable=True)