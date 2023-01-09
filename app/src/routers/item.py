from uuid import uuid4
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.src.dependencies import get_db
from app.src.models import Item
from app.src.schemas import CreateNewItem, NewItemCreated


router = APIRouter(prefix="/item", tags=["Item"])


@router.post("", response_model=NewItemCreated)
def create_item(payload: CreateNewItem, session: Session = Depends(get_db)):
    i = Item(
        id=str(uuid4()),
        access_token=payload.access_token,
        user_id=payload.user_id,
        active=True,
    )

    with session.begin():
        session.add(i)
        session.commit()

    return {"item_created": True}
