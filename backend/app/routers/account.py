import asyncio

from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Item, User
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_get_response import AccountsGetResponse
from plaid_manager import client
from sqlalchemy.orm import Session

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("")
async def get_accounts(user_id: str, session: Session = Depends(get_db)):
    with session.begin():
        user = session.query(User).filter(User.id == user_id)

        if not user:
            return HTTPException(status_code=401, detail="User Not Found")

        items: list[Item] = session.query(Item).filter(Item.user_id == user_id).all()
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
