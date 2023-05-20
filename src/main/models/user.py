import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from ..base import Base
from ..database import get_db
from ..util import get_secret


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """Google Oauth specific information for a user."""

    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Base user class, extending FastAPI-users."""

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


UserDB = SQLAlchemyUserDatabase[User, uuid.UUID]


async def get_user_db(session: AsyncSession = Depends(get_db)):
    """Return the FastAPI-users database object."""
    db: UserDB = SQLAlchemyUserDatabase(session, User, OAuthAccount)
    yield db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Define handlers for user events."""

    reset_password_token_secret = get_secret("RESET_PASSWORD_TOKEN_SECRET")
    verification_token_secret = get_secret("VERIFICATION_TOKEN_SECRET")

    async def on_after_register(self, user: User, request: Request | None = None):
        """Handle user registation event."""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        """Handle user forgot password event."""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        """Handle user verification event."""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: UserDB = Depends(get_user_db)):
    """Return an instance of the UserManager class."""
    yield UserManager(user_db)


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Pydantic schema for a user object on read."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Pydantic schema for a user object on create."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Pydantic schema for a user object on update."""

    pass
