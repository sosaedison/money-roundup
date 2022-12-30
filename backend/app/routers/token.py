from fastapi import APIRouter

from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from plaid_manager import client

from pydantic import BaseModel

class PublicTokenExchangeBody(BaseModel):
    public_token: str
    metadata: object

router = APIRouter(tags=["Link Token"])




@router.get("/link/token/create")
def link_token_create():
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
        user=LinkTokenCreateRequestUser(client_user_id="test-user-sosa"),
    )
    res = client.link_token_create(request)
    return {"link_token": res["link_token"]}

@router.post("/exchange/public/token")
def exchange_public_token(payload: PublicTokenExchangeBody):
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=payload.public_token   
    )

    exchange_response = client.item_public_token_exchange(exchange_request)

    print(exchange_response)
