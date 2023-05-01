import uuid
from typing import Any, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from .models.user import User, get_user_db
from .util import get_secret


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """The UserManager manages users? or something."""

    reset_password_token_secret = get_secret("RESET_PASSWORD_TOKEN_SECRET")
    verification_token_secret = get_secret("VERIFICATION_TOKEN_SECRET")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Handle user registration event."""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Handle user forgot password event."""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Handle user verification event."""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[User, Any] = Depends(get_user_db)
):
    """Get the UserManager."""
    yield UserManager(user_db)
