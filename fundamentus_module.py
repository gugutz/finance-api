import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_dados_fundamentus(ticker) -> dict :
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    def pegar_valor(label):
        try:
            span = soup.find('span', class_='txt', string=lambda t: t and label.lower() in t.lower())
            if not span:
                return None

            td_label = span.find_parent('td')
            td_valor = td_label.find_next_sibling('td')
            if not td_valor:
                return None

            valor_bruto = td_valor.get_text(strip=True)
            valor = valor_bruto.replace('.', '').replace(',', '.').replace('%', '')
            return valor
        except Exception:
            return None

    try:
        preco = float(pegar_valor('Cotação'))
        dy = float(pegar_valor('Div. Yield'))
        lpa = float(pegar_valor('LPA'))
        vpa = float(pegar_valor('VPA'))
        dividendos = round(preco * (dy / 100), 2)

        preco_graham = round((22.5 * lpa * vpa) ** 0.5, 2) if lpa > 0 and vpa > 0 else None
        preco_bazin = round(dividendos / 0.06, 2) if dividendos > 0 else None

        return {
            'Ticker': ticker,
            'Preço': preco,
            'DY (%)': dy,
            'LPA': lpa,
            'VPA': vpa,
            'Dividendos por Ação': dividendos,
            'Preço Graham': preco_graham,
            'Preço Bazin': preco_bazin
        }

    except Exception:
        return None

def obter_dados_fundamentus_lista(tickers):
    dados = []
    for ticker in tickers:
        info = obter_dados_fundamentus(ticker)
        if info:
            dados.append(info)

    df = pd.DataFrame(dados)
    return df

