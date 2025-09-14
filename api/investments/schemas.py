
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class RendaFixaType(str, Enum):
    CDB = "CDB"
    LCI = "LCI"
    LCA = "LCA"

class RateType(str, Enum):
    PRE = "PRE"
    POS = "POS"
    HIBRIDO = "HIBRIDO"

class IndexerType(str, Enum):
    CDI = "CDI"
    SELIC = "SELIC"
    IPCA = "IPCA"

class TermType(str, Enum):
    DIAS = "DIAS"
    DATA = "DATA"

class RendaFixaInvestment(BaseModel):
    id: Optional[str] = None
    name: str
    position: int
    type: RendaFixaType
    investedValue: float
    rateType: RateType
    indexer: Optional[IndexerType] = None
    rate: float
    extraRate: Optional[float] = None
    termType: TermType
    termValue: Optional[str] = None
    startDate: Optional[date] = None

    class Config:
        from_attributes = True

class AcaoInvestment(BaseModel):
    id: Optional[str] = None
    name: str
    position: int
    ticker: str
    quantity: int
    averagePrice: float

    class Config:
        from_attributes = True

class FIIInvestment(BaseModel):
    id: Optional[str] = None
    name: str
    position: int
    ticker: str
    quantity: int
    averagePrice: float

    class Config:
        from_attributes = True

class TesouroDiretoType(str, Enum):
    SELIC = "SELIC"
    PREFIXADO = "PREFIXADO"
    IPCA_MAIS = "IPCA+"

class TesouroDiretoInvestment(BaseModel):
    id: Optional[str] = None
    name: str
    position: int
    type: TesouroDiretoType
    investedValue: float
    rate: Optional[float] = None
    startDate: Optional[date] = None
    termDate: Optional[date] = None

    class Config:
        from_attributes = True

class CarteiraPayload(BaseModel):
    rendaFixa: List[RendaFixaInvestment]
    acoes: List[AcaoInvestment]
    fiis: List[FIIInvestment]
    tesouroDireto: List[TesouroDiretoInvestment]
