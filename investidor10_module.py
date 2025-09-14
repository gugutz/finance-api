import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

DEBUG = False

def obter_dados_investidor10(tickers):
    dados = []
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    for ticker in tickers:
        url = f"https://investidor10.com.br/acoes/{ticker}/"
        r = session.get(url)
        if r.status_code != 200:
            print(f"[{ticker}] Erro HTTP {r.status_code}")
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        # Função para extrair valor baseado no label do indicador
        def pegar_valor_indicador(label_procurado):
            # Procura por células que contenham o label
            cells = soup.find_all("div", class_="cell")
            for cell in cells:
                # Procura o span com o label
                label_span = cell.find("span", class_="d-flex justify-content-between align-items-center")
                if label_span and label_procurado.lower() in label_span.get_text().lower():
                    # Procura o div com a classe value que contém o valor
                    value_div = cell.find("div", class_="value d-flex justify-content-between align-items-center")
                    if value_div:
                        # Pega o primeiro span dentro do value_div
                        value_span = value_div.find("span")
                        if value_span:
                            valor_texto = value_span.get_text().strip()
                            # Remove espaços em branco e quebras de linha
                            valor_texto = re.sub(r'\s+', '', valor_texto)
                            return valor_texto
            return None

        # Função alternativa para extrair indicadores com estrutura diferente
        def pegar_valor_indicador_alt(label_procurado):
            # Procura por spans com title
            spans = soup.find_all("span", class_="title")
            for span in spans:
                if label_procurado.lower() in span.get_text().lower():
                    # Procura o span value no mesmo container
                    container = span.parent
                    if container:
                        value_span = container.find("span", class_="value")
                        if value_span:
                            return value_span.get_text().strip()
            return None

        # Função para extrair cotação atual
        def pegar_cotacao():
            # Procura por elementos que podem conter a cotação
            cotacao_patterns = [
                {"class": "cotacao"},
                {"class": "price"},
                {"class": "current-price"},
                {"class": "value-now"},
                {"class": "price-info"},
                {"class": "stock-price"}
            ]

            for pattern in cotacao_patterns:
                elemento = soup.find("div", pattern) or soup.find("span", pattern)
                if elemento:
                    texto = elemento.get_text().strip()
                    match = re.search(r'(\d+,\d+)', texto)
                    if match:
                        return match.group(1)

            # Procura por padrões no texto da página
            texto_completo = soup.get_text()
            # Procura por "Cotação" seguido de valor
            match = re.search(r'Cotação[^\d]*(\d+,\d+)', texto_completo, re.IGNORECASE)
            if match:
                return match.group(1)

            # Procura por "R$" seguido de número
            match = re.search(r'R\$\s*(\d+,\d+)', texto_completo)
            if match:
                return match.group(1)

            return None

        # Converte os valores para float
        def converter_valor(valor_str):
            if not valor_str:
                return None
            try:
                # Remove % se houver
                valor_str = valor_str.replace('%', '')
                # Substitui vírgula por ponto
                valor_str = valor_str.replace(',', '.')
                # Remove pontos que são separadores de milhares
                partes = valor_str.split('.')
                if len(partes) > 2:
                    # Se há mais de um ponto, o último é decimal
                    valor_str = ''.join(partes[:-1]) + '.' + partes[-1]
                return float(valor_str)
            except (ValueError, AttributeError):
                return None

        # ============= INDICADORES DE PREÇO =============
        preco = pegar_cotacao()

        # ============= INDICADORES DE VALUATION =============
        pl = pegar_valor_indicador("P/L")
        pvp = pegar_valor_indicador("P/VP") or pegar_valor_indicador("P/VPA")
        ev_ebitda = pegar_valor_indicador("EV/EBITDA")

        # ============= INDICADORES DE RENTABILIDADE =============
        dy = pegar_valor_indicador("Dividend Yield") or pegar_valor_indicador("DY")
        roe = pegar_valor_indicador("ROE")
        margem_liquida = pegar_valor_indicador("Margem Líquida") or pegar_valor_indicador("Marg. Líquida")

        # ============= INDICADORES FUNDAMENTAIS =============
        lpa = pegar_valor_indicador("LPA") or pegar_valor_indicador("Lucro por Ação")
        vpa = pegar_valor_indicador("VPA") or pegar_valor_indicador("Valor Patrimonial")

        # ============= INDICADORES DE ENDIVIDAMENTO =============
        div_liquida_ebitda = pegar_valor_indicador("Dív. Líquida/EBITDA") or pegar_valor_indicador("Divida Liquida/EBITDA")

        # ============= INDICADORES DE GOVERNANÇA =============
        tag_along = pegar_valor_indicador("Tag Along") or pegar_valor_indicador_alt("Tag Along")

        # Converte para float
        preco_float = converter_valor(preco)
        pl_float = converter_valor(pl)
        pvp_float = converter_valor(pvp)
        ev_ebitda_float = converter_valor(ev_ebitda)
        dy_float = converter_valor(dy)
        roe_float = converter_valor(roe)
        margem_liquida_float = converter_valor(margem_liquida)
        lpa_float = converter_valor(lpa)
        vpa_float = converter_valor(vpa)
        div_liquida_ebitda_float = converter_valor(div_liquida_ebitda)
        tag_along_float = converter_valor(tag_along)

        # Se não conseguiu pegar o preço, tenta calcular pelo P/L e LPA
        if not preco_float and pl_float and lpa_float:
            preco_float = round(pl_float * lpa_float, 2)

        # ============= CÁLCULOS DERIVADOS =============
        # Calcula dividendos por ação se tiver DY e preço
        dividendos_por_acao = None
        if preco_float and dy_float:
            dividendos_por_acao = round(preco_float * (dy_float / 100), 2)

        # Calcula Preço Graham: (22.5 * LPA * VPA) ^ 0.5
        preco_graham = None
        if lpa_float and vpa_float and lpa_float > 0 and vpa_float > 0:
            preco_graham = round((22.5 * lpa_float * vpa_float) ** 0.5, 2)

        # Calcula Preço Bazin: Dividendos por Ação / 0.06 (6% de yield)
        preco_bazin = None
        if dividendos_por_acao:
            preco_bazin = round(dividendos_por_acao / 0.06, 2)

        # Arredonda valores para 2 casas decimais onde necessário
        dados.append({
            # Dados básicos
            "Ticker": ticker,
            "Preço": preco_float,

            # Indicadores de Valuation
            "P/L": round(pl_float, 2) if pl_float else None,
            "P/VP": round(pvp_float, 2) if pvp_float else None,
            "EV/EBITDA": round(ev_ebitda_float, 2) if ev_ebitda_float else None,

            # Indicadores de Rentabilidade
            "DY (%)": round(dy_float, 2) if dy_float else None,
            "ROE (%)": round(roe_float, 2) if roe_float else None,
            "Margem Líquida (%)": round(margem_liquida_float, 2) if margem_liquida_float else None,

            # Indicadores Fundamentais
            "LPA": round(lpa_float, 2) if lpa_float else None,
            "VPA": round(vpa_float, 2) if vpa_float else None,

            # Indicadores de Endividamento
            "Dív. Líq./EBITDA": round(div_liquida_ebitda_float, 2) if div_liquida_ebitda_float else None,

            # Indicadores de Governança
            "Tag Along (%)": round(tag_along_float, 2) if tag_along_float else None,

            # Cálculos Derivados
            "Dividendos por Ação": dividendos_por_acao,
            "Preço Graham": preco_graham,
            "Preço Bazin": preco_bazin,
        })

        if DEBUG:
            print(f"[{ticker}] Dados extraídos:")
            print(f"  Preço: {preco_float}")
            print(f"  P/L: {pl_float}, P/VP: {pvp_float}, EV/EBITDA: {ev_ebitda_float}")
            print(f"  DY: {dy_float}%, ROE: {roe_float}%, Margem Líq.: {margem_liquida_float}%")
            print(f"  LPA: {lpa_float}, VPA: {vpa_float}")
            print(f"  Dív.Líq./EBITDA: {div_liquida_ebitda_float}")
            print(f"  Tag Along: {tag_along_float}%")

    # Retorna DataFrame
    df = pd.DataFrame(dados)
    return df

# Exemplo de uso:
# tickers = ["PETR4", "VALE3", "ITUB4"]
# df = obter_dados_investidor10(tickers)
# print(df)