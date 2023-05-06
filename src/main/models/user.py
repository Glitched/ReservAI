from typing import Any
from uuid import uuid4

from sqlalchemy import Column, String, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from ..base import Base


class User(Base):
    """Primary user object for the app."""

    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs: dict[str, Any]):
        """Create a new user."""
        transaction = cls(id=uuid4().hex, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        """Get user by ID."""
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        """Fetch all users."""
        return (await db.execute(select(cls))).scalars().all()
