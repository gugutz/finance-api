
from fastapi import APIRouter, HTTPException
from typing import Optional, List

from . import schemas, services

# Importa os módulos de scraping originais
import investidor10_module
import fundamentus_module
import yfinance_module

router = APIRouter()

DEFAULT_TICKERS = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'B3SA3', 'ELET3', 'ABEV3', 'RENT3', 'WEGE3', 'SUZB3']

@router.get("/tickers", response_model=List[schemas.TickerData], tags=["Tickers"])
async def get_tickers_data(
    source: str,
    tickers: Optional[str] = None
):
    """
    Obtém dados de tickers de uma fonte específica.

    - **source**: A fonte dos dados. Valores válidos: `investidor10`, `fundamentus`, `yfinance`.
    - **tickers**: Uma lista de tickers separados por vírgula (ex: `PETR4,VALE3`). 
                   Se não for fornecido, uma lista padrão será usada.
    """
    ticker_list = DEFAULT_TICKERS
    if tickers:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]

    source = source.lower()
    
    try:
        if source == 'investidor10':
            df = investidor10_module.obter_dados_investidor10(ticker_list)
            return services.normalize_investidor10_data(df)
        
        elif source == 'fundamentus':
            df = fundamentus_module.get_fundamentus_data(ticker_list)
            return services.normalize_fundamentus_data(df)
            
        elif source == 'yfinance':
            data_dict = yfinance_module.get_yfinance_data(ticker_list)
            return services.normalize_yfinance_data(data_dict)
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Fonte '{source}' inválida. Fontes disponíveis: investidor10, fundamentus, yfinance."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar dados da fonte '{source}': {e}"
        )
