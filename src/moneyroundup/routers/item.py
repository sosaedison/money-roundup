from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException

from moneyroundup.database import get_async_session_context_manager
from moneyroundup.users import current_active_user

from moneyroundup.models import Item
from moneyroundup.schemas import CreateNewItem


router = APIRouter(prefix="/item", tags=["Item"])


@router.post("", status_code=201)
async def create_item(payload: CreateNewItem, session = get_async_session_context_manager, user = Depends(current_active_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    i = Item(
        id=str(uuid4()),
        access_token=payload.access_token,
        user_id=payload.user_id,
        active=True,
    )

    async with session() as session:
        session.add(i)
        await session.commit()

    return {"item_created": True, "user_id": payload.user_id}
