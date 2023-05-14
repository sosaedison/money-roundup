from fastapi import APIRouter, Depends, HTTPException
from plaid.model.country_code import CountryCode
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products

from moneyroundup.plaid_manager import client
from moneyroundup.schemas import PublicTokenExchangeBody, UserFromDB
from moneyroundup.users import current_active_user

router = APIRouter(tags=["Link Token"])


@router.post("/link/token/create")
def link_token_create(
    user=Depends(current_active_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="User Not Found")

    req = LinkTokenCreateRequest(
        products=[Products("auth"), Products("transactions")],
        client_name="MoneyRoundup",
        country_codes=[CountryCode("US")],
        language="en",
        link_customization_name="default",
        account_filters=LinkTokenAccountFilters(
            depository=DepositoryFilter(
                account_subtypes=DepositoryAccountSubtypes(
                    [
                        DepositoryAccountSubtype("checking"),
                        DepositoryAccountSubtype("savings"),
                    ]
                )
            )
        ),
        user=LinkTokenCreateRequestUser(client_user_id="testuser"),
    )
    res = client.link_token_create(req)

    return {"link_token": res["link_token"]}


@router.post("/exchange/public/token")
def exchange_public_token(payload: PublicTokenExchangeBody):
    exchange_request = ItemPublicTokenExchangeRequest(public_token=payload.public_token)

    exchange_response = client.item_public_token_exchange(exchange_request)

    access_token = exchange_response["access_token"]

    return {"access_token_created": True, "access_token": access_token}
