import asyncio

from fastapi import APIRouter, Depends, HTTPException
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_get_response import AccountsGetResponse
from sqlalchemy.orm import Session

from moneyroundup.dependencies import get_current_user, get_db
from moneyroundup.models import Item, User
from moneyroundup.plaid_manager import client
from moneyroundup.schemas import UserFromDB

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("")
async def get_accounts(
    session: Session = Depends(get_db),
    user: UserFromDB | None = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="User Not Found")

    with session.begin():

        items = session.query(Item).filter(Item.user_id == user.id).all()
        access_tokens: list[str] = [i.access_token for i in items]

    account_data = []
    for access_token in access_tokens:
        request = AccountsGetRequest(access_token=access_token)
        accounts_response: AccountsGetResponse = client.accounts_get(request)

        res_as_dict = accounts_response.to_dict()
        format_accounts_response(res_as_dict, account_data)

    return account_data


def format_accounts_response(account_response: dict, account_data: list) -> None:
    for account in account_response["accounts"]:
        account_data.append({"name": account["name"]})


async def fetch_account_data(access_tokens: list):
    if not access_tokens:
        return

    async def fetch_data(access_token: str):
        request = AccountsGetRequest(access_token=access_token)
        accounts_response = client.accounts_get(request)

        return accounts_response.to_dict()

    data = []
    account_tasks = []
    for token in access_tokens:
        account_tasks.append(asyncio.create_task(fetch_data(access_token=token)))

    done, _ = await asyncio.wait(account_tasks)

    for task in done:
        data.append(await task)

    return data


async def sanitize_data(connections):
    # connections = raw_data
    ret = []
    for bank_connection in connections:
        bank_accounts = bank_connection["accounts"]
        bank_data = {"items": []}
        for account in bank_accounts:
            bank_data["items"].append({"name": account["name"]})
        ret.append(bank_data)

    return ret[0]
