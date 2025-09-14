import pandas as pd
import plotly.graph_objects as go

def gerar_html(dados):
    df = pd.DataFrame(dados)
    df.fillna("", inplace=True)


    # Tabela formatada como HTML
    # tabela_html = df.to_html(index=False, float_format="%.2f", classes="table table-striped", border=0)
    tabela_html = df.to_html(index=False, float_format="%.2f", classes='table table-striped', border=0)


    # Gráfico de Preço por Ticker
    fig_preco = go.Figure([go.Bar(x=df["Ticker"], y=df["Preço"], name="Preço")])
    fig_preco.update_layout(title="Preço por Ação", xaxis_title="Ticker", yaxis_title="Preço (R$)")

    # Gráfico de DY (%) por Ticker
    fig_dy = go.Figure([go.Bar(x=df["Ticker"], y=df["DY (%)"], name="Dividend Yield (%)", marker_color="green")])
    fig_dy.update_layout(title="Dividend Yield (%)", xaxis_title="Ticker", yaxis_title="DY (%)")

    # Salvar HTML completo
    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Ações</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body class="p-4">
            <h1>Relatório de Análise de Ações</h1>
            <h2>Tabela de Dados Fundamentus</h2>
            {tabela_html}
            <h2 class="mt-5">Gráfico: Preço por Ação</h2>
            <div id="grafico_preco">{fig_preco.to_html(include_plotlyjs=False, full_html=False)}</div>
            <h2 class="mt-5">Gráfico: Dividend Yield (%)</h2>
            <div id="grafico_dy">{fig_dy.to_html(include_plotlyjs=False, full_html=False)}</div>
        </body>
        </html>
        """)

    print("✅ HTML salvo como relatorio.html — pode abrir no navegador e dar reload sempre que rodar o script.")