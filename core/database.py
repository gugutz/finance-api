
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Database URL - Connects to the PostgreSQL container
# FORMAT: postgresql+asyncpg://USER:PASSWORD@HOST/DATABASE
DATABASE_URL = "postgresql+asyncpg://finance_user:finance_password@localhost/finance_db"

# Create an async engine
engine = create_async_engine(DATABASE_URL)

# Create a session maker
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class for our models
Base = declarative_base()

# Dependency to get a DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
