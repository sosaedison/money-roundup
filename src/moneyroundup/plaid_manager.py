import plaid
from plaid.api import plaid_api

from moneyroundup.settings import get_settings

settings = get_settings()

# Available environments are
# 'Production'
# 'Development'
# 'Sandbox'
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        "clientId": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SANDBOX_KEY,
    },
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
