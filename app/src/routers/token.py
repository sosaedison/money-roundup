from fastapi import APIRouter, Depends, HTTPException

from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)

from app.src.plaid_manager import client
from app.src.dependencies import get_db
from app.src.models import User
from app.src.schemas import PublicTokenExchangeBody, UserRequestingLinkToken

from sqlalchemy.orm import Session

router = APIRouter(tags=["Link Token"])


@router.post("/link/token/create")
def link_token_create(
    user: UserRequestingLinkToken, session: Session = Depends(get_db)
):
    with session.begin():
        u = session.query(User).filter(User.id == user.user_id).first()

    if not u:
        raise HTTPException(status_code=401, detail="User does not exist")

    request = LinkTokenCreateRequest(
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
        user=LinkTokenCreateRequestUser(client_user_id=user.user_id),
    )
    res = client.link_token_create(request)
    return {"link_token": res["link_token"], "user_id": user.user_id}


@router.post("/exchange/public/token")
def exchange_public_token(payload: PublicTokenExchangeBody):
    exchange_request = ItemPublicTokenExchangeRequest(public_token=payload.public_token)

    exchange_response = client.item_public_token_exchange(exchange_request)

    access_token = exchange_response["access_token"]

    return {"access_token_created": True, "access_token": access_token}
