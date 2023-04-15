from unittest.mock import patch
from uuid import uuid4

from pytest import fixture
from sqlalchemy.orm import Session

from moneyroundup.base import Base
from moneyroundup.database import engine
from moneyroundup.dependencies import get_db
from moneyroundup.fetch_transactions import populate_queue_with_transactions
from moneyroundup.models import Item, UserOld
from moneyroundup.plaid_manager import client
from moneyroundup.rabbit_manager import QueueManager, RabbitManager


@fixture(scope="function", autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_user = UserOld(
        id=str(uuid4()),
        email="sosarocks@test.com",
        first_name="Sosa",
        last_name="Rocks",
        profile_pic_url="http://www.some_cool_pic.com",
    )

    db = get_db()
    session: Session = next(db)

    with session.begin():
        session.add(new_user)
        session.commit()


@fixture()
def database_session():
    db = get_db()
    session: Session = next(db)
    return session


@fixture()
def test_queue_manager():
    class TestQueueManager:
        # this class acts as a mock for the RabbitManager class
        def __init__(self) -> None:
            self.queue: list[str] = []

        def consume(self) -> str:
            ...

        def produce(self, message: str) -> bool:
            self.queue.append(message)
            return True

    return TestQueueManager()


def test_populate_queue_with_transactions(test_queue_manager, database_session):
    # create test QueueManager
    rabbit = test_queue_manager

    # create test database session
    session: Session = database_session

    # create test Item with access_token
    access_token = "test_access_token"
    with session.begin():
        user: UserOld | None = (
            session.query(UserOld).filter(UserOld.first_name == "Sosa").first()
        )
        if user is not None:
            i = Item(
                id=str(uuid4()),
                access_token=access_token,
                user_id=user.id,
                active=True,
            )

            session.add(i)
            session.commit()

    # create test transaction for plaid response
    plaid_client_response = {"total_transactions": 0}
    with patch.object(client, "transactions_get", return_value=plaid_client_response):
        populate_queue_with_transactions(rabbit, session)

    assert len(rabbit.queue) == 1
