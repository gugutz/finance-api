
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import User
from core.security import get_password_hash
from .schemas import UserCreate

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetches a user from the database by email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
