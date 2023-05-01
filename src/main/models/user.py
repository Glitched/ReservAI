# from sqlalchemy import Column, String, select
# from sqlalchemy.exc import NoResultFound
import uuid
from typing import Any, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from main.database import Base, get_db
from main.util import get_secret
from sqlalchemy.ext.asyncio import AsyncSession


class User(SQLAlchemyBaseUserTableUUID, Base):
    """fastapi-users base class."""

    pass


async def get_user_db(
    session: AsyncSession = Depends(get_db),
):
    """get_user_db returns the fastapi-users."""
    udb: SQLAlchemyUserDatabase[User, Any] = SQLAlchemyUserDatabase(session, User)
    yield udb


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


# class UserOld(Base):
#     """Primary user object for the app."""

#     __tablename__ = "users"
#     id = Column(String, primary_key=True)
#     email = Column(String, unique=True, nullable=False)
#     full_name = Column(String, nullable=False)

#     @classmethod
#     async def create(
#         cls, db: AsyncSession, id: str | None = None, **kwargs: dict[str, Any]
#     ):
#         """Create a new user."""
#         if not id:
#             id = uuid4().hex

#         transaction = cls(id=id, **kwargs)
#         db.add(transaction)
#         await db.commit()
#         await db.refresh(transaction)
#         return transaction

#     @classmethod
#     async def get(cls, db: AsyncSession, id: str):
#         """Get user by ID."""
#         try:
#             transaction = await db.get(cls, id)
#         except NoResultFound:
#             return None
#         return transaction

#     @classmethod
#     async def get_all(cls, db: AsyncSession):
#         """Fetch all users."""
#         return (await db.execute(select(cls))).scalars().all()
