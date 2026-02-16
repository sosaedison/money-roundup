from fastapi import APIRouter, Depends

from moneyroundup.auth import SupabaseUser, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def me(user: SupabaseUser = Depends(get_current_user)):
    """Return the current authenticated user's info."""
    return {"id": user.id, "email": user.email}
