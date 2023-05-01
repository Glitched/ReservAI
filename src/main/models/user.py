# from sqlalchemy import Column, String, select
# from sqlalchemy.exc import NoResultFound

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declarative_base, relationship

from ..database import get_db

Base = declarative_base()


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """Adapter so we can use sign in with google."""

    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """fastapi-users base class."""

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


async def get_user_db(
    session: AsyncSession = Depends(get_db),
):
    """get_user_db returns the fastapi-users."""
    udb: SQLAlchemyUserDatabase[User, OAuthAccount] = SQLAlchemyUserDatabase(
        session, User, OAuthAccount
    )
    yield udb


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
