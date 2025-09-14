from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    renda_fixa = relationship("RendaFixaInvestment", back_populates="owner", cascade="all, delete-orphan")
    acoes = relationship("AcaoInvestment", back_populates="owner", cascade="all, delete-orphan")
    fiis = relationship("FIIInvestment", back_populates="owner", cascade="all, delete-orphan")
    tesouro_direto = relationship("TesouroDiretoInvestment", back_populates="owner", cascade="all, delete-orphan")


class RendaFixaType(enum.Enum):
    CDB = "CDB"
    LCI = "LCI"
    LCA = "LCA"

class RateType(enum.Enum):
    PRE = "PRE"
    POS = "POS"
    HIBRIDO = "HIBRIDO"

class IndexerType(enum.Enum):
    CDI = "CDI"
    SELIC = "SELIC"
    IPCA = "IPCA"

class TermType(enum.Enum):
    DIAS = "DIAS"
    DATA = "DATA"

class RendaFixaInvestment(Base):
    __tablename__ = "renda_fixa"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(Integer)
    type = Column(Enum(RendaFixaType))
    investedValue = Column(Numeric(10, 2))
    rateType = Column(Enum(RateType))
    indexer = Column(Enum(IndexerType), nullable=True)
    rate = Column(Numeric(10, 2))
    extraRate = Column(Numeric(10, 2), nullable=True)
    termType = Column(Enum(TermType))
    termValue = Column(String, nullable=True) # Can be date or days
    startDate = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="renda_fixa")


class AcaoInvestment(Base):
    __tablename__ = "acoes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(Integer)
    ticker = Column(String, index=True)
    quantity = Column(Integer)
    averagePrice = Column(Numeric(10, 2))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="acoes")


class FIIInvestment(Base):
    __tablename__ = "fiis"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(Integer)
    ticker = Column(String, index=True)
    quantity = Column(Integer)
    averagePrice = Column(Numeric(10, 2))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="fiis")


class TesouroDiretoType(enum.Enum):
    SELIC = "SELIC"
    PREFIXADO = "PREFIXADO"
    IPCA_MAIS = "IPCA+"

class TesouroDiretoInvestment(Base):
    __tablename__ = "tesouro_direto"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(Integer)
    type = Column(Enum(TesouroDiretoType))
    investedValue = Column(Numeric(10, 2))
    rate = Column(Numeric(10, 2), nullable=True)
    startDate = Column(Date, nullable=True)
    termDate = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tesouro_direto")