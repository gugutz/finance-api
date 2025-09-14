
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import settings

# Create an async engine using the URL from settings
engine = create_async_engine(settings.DATABASE_URL)

# Create a session maker
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class for our models
Base = declarative_base()

# Dependency to get a DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
