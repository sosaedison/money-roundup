from fastapi import APIRouter, Depends, HTTPException
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_get_response import AccountsGetResponse

from moneyroundup.auth import SupabaseUser, get_current_user
from moneyroundup.plaid_manager import client
from moneyroundup.supabase_client import supabase

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("")
def get_accounts(user: SupabaseUser = Depends(get_current_user)):
    result = (
        supabase.table("items")
        .select("access_token")
        .eq("user_id", user.id)
        .eq("active", True)
        .execute()
    )

    access_tokens: list[str] = [row["access_token"] for row in result.data]

    account_data = []
    for access_token in access_tokens:
        request = AccountsGetRequest(access_token=access_token)
        accounts_response: AccountsGetResponse = client.accounts_get(request)
        res_as_dict = accounts_response.to_dict()
        for account in res_as_dict["accounts"]:
            account_data.append({"name": account["name"]})

    return account_data
