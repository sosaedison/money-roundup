import asyncio
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from models import User, Item
from plaid_manager import client
from dependencies import get_db

from plaid.model.accounts_get_request import AccountsGetRequest

router  = APIRouter(prefix="/account", tags=["Account"])

@router.get("")
async def get_accounts(user_id: str, session: Session = Depends(get_db)):
    """
        - validate the user
        - if not user, then return error
        - fetch the access_tokens for active items with that user_id
        - async fetch accounts info for each access_token
        - as requests get resolved, build return obj
        - return data
    """
    with session.begin():
        user = session.query(User).filter(User.id == user_id)

        if not user:
            return HTTPException(status_code=401, detail="User Not Found")

        items = session.query(Item).filter(Item.user_id == user_id).all()
        access_tokens = [i.access_token for i in items]

    raw_data = await fetch_account_data(access_tokens=access_tokens)
    clean_data = await sanitize_data(raw_data)

    print(clean_data)
    return clean_data

async def fetch_account_data(access_tokens: list):
    if not access_tokens:
        return

    async def fetch_data(access_token:str):
        request = AccountsGetRequest(
          access_token=access_token
        )
        accounts_response = client.accounts_get(request)

        return accounts_response.to_dict()

    data = []
    account_tasks = []
    for token in access_tokens:
        account_tasks.append(asyncio.create_task(fetch_data(access_token=token)))

    done, _ = await asyncio.wait(account_tasks)

    for task in done:
        data.append(await task)

    """
    [
        {
            items: [
                {
                    name: ""
                    balances: {
                        available
                        current
                },
            ],
            active
        },
        {
            items: [
                {
                    name: "",
                    balances: {
                        available
                        current
                    }
                }
            ]
        }
    ]
    """
    return data

async def sanitize_data(connections):
    # connections = raw_data
    ret = []
    for bank_connection in connections:
        bank_accounts = bank_connection["accounts"]
        bank_data = {"items":[]}
        for account in bank_accounts:
            bank_data["items"].append({"name": account["name"]})
        ret.append(bank_data)

    return ret[0]