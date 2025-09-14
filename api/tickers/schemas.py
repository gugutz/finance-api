
from pydantic import BaseModel
from typing import Optional

class TickerData(BaseModel):
    """Data structure for ticker information from all sources."""
    ticker: str
    long_name: Optional[str] = None
    
    # Price and Value
    preco: Optional[float] = None
    book_value: Optional[float] = None
    market_cap: Optional[float] = None
    patrimonio_liq: Optional[float] = None
    
    # Ratios
    p_l: Optional[float] = None
    p_vp: Optional[float] = None
    psr: Optional[float] = None
    p_ativo: Optional[float] = None
    p_cap_giro: Optional[float] = None
    p_ebit: Optional[float] = None
    p_ativ_circ_liq: Optional[float] = None
    
    # Enterprise Value
    ev_ebit: Optional[float] = None
    ev_ebitda: Optional[float] = None
    
    # Dividends
    dy: Optional[float] = None
    
    # Debt
    div_liquida_ebit: Optional[float] = None
    div_liq_patri: Optional[float] = None
    div_brut_patrim: Optional[float] = None
    
    # Margins
    margem_bruta: Optional[float] = None
    margem_ebit: Optional[float] = None
    margem_liquida: Optional[float] = None
    
    # Liquidity
    liquidez_corrente: Optional[float] = None
    liq_2meses: Optional[float] = None
    
    # Profitability / Return
    roic: Optional[float] = None
    roe: Optional[float] = None
    
    # Growth
    cagr_lucros_5_anos: Optional[float] = None
    cagr_receitas_5_anos: Optional[float] = None
    
    # Valuation Models
    graham: Optional[float] = None
    graham_vs_preco: Optional[str] = None
    bazin: Optional[float] = None
    bazin_vs_preco: Optional[str] = None
    
    # Yahoo Finance Specific
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    average_daily_volume_10_day: Optional[int] = None

    class Config:
        from_attributes = True
