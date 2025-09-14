from collections import defaultdict
import itertools
import pandas as pd

# Utilidade para extrair a base de um ticker (ex: 'PETR3' → 'PETR')
def extrair_base(ticker):
    return ''.join([c for c in ticker if not c.isdigit()])

# Calcula defasagem percentual entre dois preços
def calcular_defasagem(preco_a, preco_b):
    return round(((preco_a / preco_b) - 1) * 100, 2)

# Gera um resumo de defasagem entre tickers da mesma empresa
def exibir_resumo_defasagem(dados):
    print("\n" + "="*80)
    print("Resumo de Defasagem por Empresa (mesmo grupo de ticker):")

    # Agrupar por base
    grupos = defaultdict(list)
    for d in dados:
        base = extrair_base(d['Ticker'])
        grupos[base].append(d)

    for base, tickers in grupos.items():
        if len(tickers) <= 1:
            continue

        print(f"\nGrupo {base}:")
        melhores = []

        # Ordenar pares e comparar preços
        for a, b in itertools.combinations(tickers, 2):
            defasagem = calcular_defasagem(a['Preço'], b['Preço'])
            if defasagem > 0:
                print(f"- {a['Ticker']} está {defasagem:.2f}% mais caro que {b['Ticker']}")
                melhores.append((b['Ticker'], defasagem))
            elif defasagem < 0:
                print(f"- {b['Ticker']} está {abs(defasagem):.2f}% mais caro que {a['Ticker']}")
                melhores.append((a['Ticker'], abs(defasagem)))
            else:
                print(f"- {a['Ticker']} e {b['Ticker']} estão com o mesmo preço.")

        # Ticker com maior recorrência como "mais barato"
        if melhores:
            recomendacoes = pd.Series([m[0] for m in melhores]).value_counts()
            melhor_opcao = recomendacoes.idxmax()
            print(f"🔍 Melhor escolha relativa: {melhor_opcao}")
