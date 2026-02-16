from fastapi import APIRouter, Depends, HTTPException

from moneyroundup.auth import SupabaseUser, get_current_user
from moneyroundup.schemas import CreateNewItem
from moneyroundup.supabase_client import supabase

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("", status_code=201)
def create_item(
    payload: CreateNewItem,
    user: SupabaseUser = Depends(get_current_user),
):
    result = (
        supabase.table("items")
        .insert({"user_id": user.id, "access_token": payload.access_token})
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create item")

    return {"item_created": True, "user_id": user.id}
