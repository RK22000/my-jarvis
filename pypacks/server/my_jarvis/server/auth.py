import os
from typing import Optional, Set, TypedDict

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from authlib.integrations.base_client.errors import MismatchingStateError, MissingTokenError

router = APIRouter()


def get_env_var(key: str) -> str:
    value: Optional[str] = os.getenv(key)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# Load and validate environment variables
GOOGLE_CLIENT_ID: str = get_env_var("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: str = get_env_var("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI: str = get_env_var("GOOGLE_REDIRECT_URI")
MIDDLEWARE_KEY: str = get_env_var("MIDLEWARE_KEY")

# Type for parsed user info
class GoogleUserInfo(TypedDict):
    email: str
    name: Optional[str]


# Set up OAuth
oauth: OAuth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@router.get("/auth/callback")
async def auth_callback(request: Request) -> GoogleUserInfo:
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info: GoogleUserInfo = await oauth.google.parse_id_token(request, token)
    except (OAuthError, MismatchingStateError, MissingTokenError, ValueError) as e:
        raise HTTPException(status_code=400, detail="Invalid Google login")

    # 🔐 Restrict access to specific emails
    allowed_users: Set[str] = {"your.email@example.com"}
    if user_info["email"] not in allowed_users:
        raise HTTPException(status_code=403, detail="Access denied")

    return {"email": user_info["email"], "name": user_info.get("name")}
