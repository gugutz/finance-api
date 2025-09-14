import requests
import pandas as pd
import numpy as np

acoes = ['PETR4', 'ITUB4', 'BBAS3']

def obter_dados_api_statusinvest(ticker):
    url = f"https://statusinvest.com.br/acao/getbasicinfo/{ticker.upper()}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers)
        print(f"Dados {ticker}:", r.json())  # Pra debug

        dados = [obter_dados_api_statusinvest(ticker) for ticker in acoes]
        print(dados)  # Pra ver exatamente o que veio para cada ticker
        df = pd.DataFrame(dados)
        print(df.columns)  # Pra ver as colunas que foram criadas

        if r.status_code != 200:
            return {"Ticker": ticker, "Erro": "Ticker não encontrado"}

        json = r.json()
        print(f"JSON: {json}")

        # return {
        #     "Ticker": ticker.upper(),
        #     "Preço": json.get("price", None),
        #     "DY (%)": json.get("dividendyield", None),
        #     "LPA": json.get("lpa", None),
        #     "VPA": json.get("vpa", None)
        # }


    except Exception as e:
        return {"Ticker": ticker.upper(), "Erro": str(e)}

dados = [obter_dados_api_statusinvest(ticker) for ticker in acoes]
df = pd.DataFrame(dados)

# df['Preço Graham'] = np.where(
#     df[['LPA', 'VPA']].notnull().all(axis=1),
#     (22.5 * df['LPA'] * df['VPA']) ** 0.5,
#     None
# )

# df['Dividendos por Ação'] = np.where(
#     df[['DY (%)', 'Preço']].notnull().all(axis=1),
#     df['DY (%)'] * df['Preço'] / 100,
#     None
# )

# df['Preço Bazin'] = np.where(
#     df['Dividendos por Ação'].notnull(),
#     df['Dividendos por Ação'] / 0.06,
#     None
# )

print(df.to_markdown(index=False))
