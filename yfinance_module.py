import yfinance as yf
import pandas as pd

DEBUG = False

def obter_dados_yfinance(tickers):
    dados = []

    for ticker in tickers:
        ticker_yf = ticker.lower() + '.sa'  # adiciona sufixo .sa aqui
        try:
            acao = yf.Ticker(ticker_yf)
            info = acao.info
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 404:
                print(f"HTTP Error 404: Ticker '{ticker_yf}' não encontrado.")
                continue
            else:
                print(f"Erro inesperado para {ticker_yf}: {e}")
                continue

        # ============= INDICADORES DE PREÇO =============
        preco = info.get('regularMarketPrice') or info.get('currentPrice')

        # ============= INDICADORES DE VALUATION =============
        pl = info.get('trailingPE')  # P/L
        pvp = info.get('priceToBook')  # P/VP
        ev_ebitda = info.get('enterpriseToEbitda')  # EV/EBITDA (pode não estar disponível)

        # ============= INDICADORES DE RENTABILIDADE =============
        roe = info.get('returnOnEquity')  # ROE
        dividend_yield = info.get('dividendYield')  # DY já em decimal
        trailing_dividend_rate = info.get('trailingAnnualDividendRate')
        profit_margins = info.get('profitMargins')  # Margem Líquida

        # ============= INDICADORES FUNDAMENTAIS =============
        lpa = info.get('trailingEps')  # LPA
        vpa = info.get('bookValue')  # VPA

        # ============= INDICADORES DE ENDIVIDAMENTO =============
        # Dívida Líquida/EBITDA não está diretamente disponível no yfinance
        # Podemos tentar calcular ou deixar como None
        total_debt = info.get('totalDebt')
        total_cash = info.get('totalCash')
        enterprise_value = info.get('enterpriseValue')

        # ============= INDICADORES DE GOVERNANÇA =============
        # Tag Along não está disponível no yfinance para ações brasileiras
        tag_along = None  # Não disponível no yfinance

        # ============= CONVERSÕES E CÁLCULOS =============
        # Converte ROE de decimal para percentual
        roe_percent = round(roe * 100, 2) if roe else None

        # Calcula DY em percentual se não estiver disponível ou usar trailing dividend rate
        if dividend_yield:
            dy_percent = round(dividend_yield * 100, 2)
        elif trailing_dividend_rate and preco:
            dy_percent = round((trailing_dividend_rate / preco) * 100, 2)
        else:
            dy_percent = None

        # Converte margem líquida para percentual
        margem_liquida_percent = round(profit_margins * 100, 2) if profit_margins else None

        # Calcula Dívida Líquida (aproximação)
        divida_liquida = None
        if total_debt and total_cash:
            divida_liquida = total_debt - total_cash

        # Tentativa de calcular Dív. Líquida/EBITDA (aproximação)
        div_liquida_ebitda = None
        # Como não temos EBITDA direto, deixamos None por enquanto

        # ============= CÁLCULOS DERIVADOS =============
        # Dividendos por ação
        dividendos_por_acao = trailing_dividend_rate

        # Calcula Preço Graham: (22.5 * LPA * VPA) ^ 0.5
        preco_graham = None
        if lpa and vpa and lpa > 0 and vpa > 0:
            preco_graham = round((22.5 * lpa * vpa) ** 0.5, 2)

        # Calcula Preço Bazin: Dividendos por Ação / 0.06 (6% de yield)
        preco_bazin = None
        if dividendos_por_acao:
            preco_bazin = round(dividendos_por_acao / 0.06, 2)

        # Monta o dicionário de dados
        dados.append({
            # Dados básicos
            "Ticker": ticker,
            "Preço": round(preco, 2) if preco else None,

            # Indicadores de Valuation
            "P/L": round(pl, 2) if pl else None,
            "P/VP": round(pvp, 2) if pvp else None,
            "EV/EBITDA": round(ev_ebitda, 2) if ev_ebitda else None,

            # Indicadores de Rentabilidade
            "DY (%)": dy_percent,
            "ROE (%)": roe_percent,
            "Margem Líquida (%)": margem_liquida_percent,

            # Indicadores Fundamentais
            "LPA": round(lpa, 2) if lpa else None,
            "VPA": round(vpa, 2) if vpa else None,

            # Indicadores de Endividamento
            "Dív. Líq./EBITDA": div_liquida_ebitda,  # Não disponível no yfinance

            # Indicadores de Governança
            "Tag Along (%)": tag_along,  # Não disponível no yfinance

            # Cálculos Derivados
            "Dividendos por Ação": round(dividendos_por_acao, 2) if dividendos_por_acao else None,
            "Preço Graham": preco_graham,
            "Preço Bazin": preco_bazin,
        })

        # Print para debug (similar ao do investidor10)
        if DEBUG:
            print(f"[{ticker}] Dados extraídos do yfinance:")
            print(f"  Preço: {preco}")
            print(f"  P/L: {pl}, P/VP: {pvp}, EV/EBITDA: {ev_ebitda}")
            print(f"  DY: {dy_percent}%, ROE: {roe_percent}%, Margem Líq.: {margem_liquida_percent}%")
            print(f"  LPA: {lpa}, VPA: {vpa}")
            print(f"  Dív.Líq./EBITDA: N/D (não disponível)")
            print(f"  Tag Along: N/D (não disponível)")

    # Retorna DataFrame
    df = pd.DataFrame(dados)
    return df

# Exemplo de uso:
# tickers = ["BBAS3", "PETR4", "VALE3"]
# df = obter_dados_yfinance(tickers)
# print(df)