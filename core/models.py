
from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    investments = relationship("FixedIncomeInvestment", back_populates="owner")


class FixedIncomeInvestment(Base):
    __tablename__ = "fixed_income_investments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    initial_value = Column(Numeric(10, 2), nullable=False)
    investment_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    indexer_type = Column(String, nullable=False) # POS, PRE, IPCA
    rate = Column(Numeric(10, 2), nullable=False)
    has_daily_liquidity = Column(Boolean, default=False, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="investments")
