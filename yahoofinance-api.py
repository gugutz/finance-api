import yfinance_module as yf
import pandas as pd

acoes = ['PETR4.SA', 'ITUB4.SA', 'BBAS3.SA']
dados = []

for ticker in acoes:
    acao = yf.Ticker(ticker)
    info = acao.info

    preco = info.get('regularMarketPrice')

    lpa = info.get('trailingEps')
    vpa = info.get('bookValue')

    # Usar trailingAnnualDividendRate como principal base
    dividendos_por_acao = info.get('trailingAnnualDividendRate')

    # Calcular DY real com base nesses dividendos e o preço atual
    dy = round((dividendos_por_acao / preco) * 100, 2) if dividendos_por_acao and preco else None

    # Preço Graham
    preco_graham = round((22.5 * lpa * vpa) ** 0.5, 2) if lpa and vpa and lpa > 0 and vpa > 0 else None

    # Preço Bazin com base nos dividendos reais
    preco_bazin = round(dividendos_por_acao / 0.06, 2) if dividendos_por_acao else None

    dados.append({
        "Ticker": ticker,
        "Preço": preco,
        "DY (%)": dy,
        "LPA": round(lpa, 2) if lpa else None,
        "VPA": round(vpa, 2) if vpa else None,
        "Dividendos por Ação": round(dividendos_por_acao, 2) if dividendos_por_acao else None,
        "Preço Graham": preco_graham,
        "Preço Bazin": preco_bazin,
    })

df = pd.DataFrame(dados)
print(df.to_markdown(index=False))
