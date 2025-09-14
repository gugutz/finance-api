
import math
import pandas as pd
from typing import Optional, List

from .schemas import TickerData

def safe_float_conversion(value) -> Optional[float]:
    """Converts a value to float safely, handling %, commas, and NaN values."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned_value = str(value).replace('%', '').strip()
        if '.' in cleaned_value and ',' in cleaned_value:
            cleaned_value = cleaned_value.replace('.', '')
        cleaned_value = cleaned_value.replace(',', '.')
        return float(cleaned_value)
    except (ValueError, TypeError):
        return None

def normalize_investidor10_data(df: pd.DataFrame) -> List[TickerData]:
    """Converts the Investidor10 DataFrame to a list of TickerData."""
    data_list = []
    for _, row in df.iterrows():
        data = TickerData(
            ticker=row.get('Ticker'),
            preco=safe_float_conversion(row.get('Preço')),
            dy=safe_float_conversion(row.get('DY (%)')),
            p_l=safe_float_conversion(row.get('P/L')),
            p_vp=safe_float_conversion(row.get('P/VP')),
            ev_ebit=safe_float_conversion(row.get('EV/EBITDA')),
            roe=safe_float_conversion(row.get('ROE (%)')),
            margem_liquida=safe_float_conversion(row.get('Margem Líquida (%)')),
            div_liq_patri=safe_float_conversion(row.get('Dív. Líq./EBITDA')),
            bazin=safe_float_conversion(row.get('Preço Bazin')),
            graham=safe_float_conversion(row.get('Preço Graham'))
        )
        data_list.append(data)
    return data_list

def normalize_fundamentus_data(df: pd.DataFrame) -> List[TickerData]:
    """Converts the Fundamentus DataFrame to a list of TickerData."""
    data_list = []
    for ticker, row in df.iterrows():
        data = TickerData(
            ticker=ticker,
            preco=safe_float_conversion(row.get('Cotação')),
            p_l=safe_float_conversion(row.get('P/L')),
            p_vp=safe_float_conversion(row.get('P/VP')),
            psr=safe_float_conversion(row.get('PSR')),
            dy=safe_float_conversion(row.get('Div.Yield')),
            p_ativo=safe_float_conversion(row.get('P/Ativo')),
            p_cap_giro=safe_float_conversion(row.get('P/Cap.Giro')),
            p_ebit=safe_float_conversion(row.get('P/EBIT')),
            p_ativ_circ_liq=safe_float_conversion(row.get('P/Ativ Circ.Liq')),
            ev_ebit=safe_float_conversion(row.get('EV/EBIT')),
            ev_ebitda=safe_float_conversion(row.get('EV/EBITDA')),
            margem_ebit=safe_float_conversion(row.get('Mrg Ebit')),
            margem_liquida=safe_float_conversion(row.get('Mrg. Líq.')),
            liquidez_corrente=safe_float_conversion(row.get('Liq. Corr.')),
            roic=safe_float_conversion(row.get('ROIC')),
            roe=safe_float_conversion(row.get('ROE')),
            liq_2meses=safe_float_conversion(row.get('Liq.2meses')),
            patrimonio_liq=safe_float_conversion(row.get('Patrim. Líq')),
            div_brut_patrim=safe_float_conversion(row.get('Dív.Brut/ Patrim.')),
            cagr_receitas_5_anos=safe_float_conversion(row.get('Cresc. Rec.5a'))
        )
        data_list.append(data)
    return data_list

def normalize_yfinance_data(data_dict: dict) -> List[TickerData]:
    """Converts the yfinance dictionary to a list of TickerData."""
    data_list = []
    for ticker, info in data_dict.items():
        if not info:
            continue
        data = TickerData(
            ticker=ticker,
            long_name=info.get('longName'),
            preco=safe_float_conversion(info.get('currentPrice')),
            dy=safe_float_conversion(info.get('dividendYield')),
            book_value=safe_float_conversion(info.get('bookValue')),
            p_vp=safe_float_conversion(info.get('priceToBook')),
            trailing_pe=safe_float_conversion(info.get('trailingPE')),
            forward_pe=safe_float_conversion(info.get('forwardPE')),
            market_cap=safe_float_conversion(info.get('marketCap')),
            fifty_two_week_high=safe_float_conversion(info.get('fiftyTwoWeekHigh')),
            fifty_two_week_low=safe_float_conversion(info.get('fiftyTwoWeekLow')),
            average_daily_volume_10_day=info.get('averageDailyVolume10Day')
        )
        data_list.append(data)
    return data_list
