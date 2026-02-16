import logging

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from moneyroundup.settings import settings

logger = logging.getLogger(__name__)

# Fetch public keys from Supabase JWKS endpoint for ES256 verification
_jwks_client = jwt.PyJWKClient(f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json")

# This tells Swagger UI to show the "Authorize" button with a Bearer token input
_bearer_scheme = HTTPBearer()


class SupabaseUser(BaseModel):
    id: str
    email: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> SupabaseUser:
    """Extract and validate the Supabase JWT from the Authorization header."""
    token = credentials.credentials

    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, jwt.exceptions.PyJWKClientError) as e:
        logger.error(f"JWT validation failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    return SupabaseUser(id=payload["sub"], email=payload.get("email", ""))
