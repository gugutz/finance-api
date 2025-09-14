import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def obter_dados_fundamentus(ticker):
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    print(f"[{ticker}] Status:", response.status_code)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    def pegar_valor(label):
        try:
            span = soup.find('span', class_='txt', string=lambda t: t and label.lower() in t.lower())
            if not span:
                print(f"[{ticker}] Label '{label}' não encontrado.")
                return None

            td_label = span.find_parent('td')
            td_valor = td_label.find_next_sibling('td')
            if not td_valor:
                print(f"[{ticker}] Valor para '{label}' não encontrado.")
                return None

            valor_bruto = td_valor.get_text(strip=True)
            print(f"[{ticker}] {label}: {valor_bruto}")
            valor = valor_bruto.replace('.', '').replace(',', '.').replace('%', '')
            return valor
        except Exception as e:
            print(f"[{ticker}] Erro ao extrair '{label}': {e}")
            return None

    try:
        preco = float(pegar_valor('Cotação'))
        dy = float(pegar_valor('Div. Yield'))
        lpa = float(pegar_valor('LPA'))
        vpa = float(pegar_valor('VPA'))
        dividendos = round(preco * (dy / 100), 2)

        preco_graham = round((22.5 * lpa * vpa) ** 0.5, 2) if lpa > 0 and vpa > 0 else ''
        preco_bazin = round(dividendos / 0.06, 2) if dividendos > 0 else ''

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

    except Exception as err:
        print(f"[{ticker}] Erro nos cálculos: {err}")
        return None



# 🧪 Teste com lista de ações
tickers = ['PETR4', 'ITUB4', 'BBAS3']

dados = []
for ticker in tickers:
    info = obter_dados_fundamentus(ticker)
    if info:
        dados.append(info)

# 📊 Mostrar tabela
print("RESULTS:")
print(tabulate(dados, headers='keys', tablefmt='github', floatfmt=".2f"))
