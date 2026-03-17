import plotly.express as px
import plotly.io as pio
from jinja2 import Template
import pandas as pd
from datetime import datetime

def generar_grafico_categorias(df_categorias):
    fig = px.bar(
        df_categorias,
        x='category',
        y=['ventas_anterior', 'ventas_actual'],
        barmode='group',
        color_discrete_map={
            'ventas_actual': "#00B4C8",
            'ventas_anterior': "#3264B0"
        },
        labels={'value': 'Ventas ($)', 'category': 'Categoría'}
    )
    fig.update_layout(
        paper_bgcolor='#0f1117',
        plot_bgcolor='#1a1d2e',
        font_color='#ffffff',
        legend_title_text=''
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_regiones(df_regiones):
    fig = px.bar(
        df_regiones,
        x='region',
        y='variacion_vs_historico',
        color='variacion_vs_historico',
        color_continuous_scale=["#FC9C27", '#00C896'],
        labels={'variacion_vs_historico': 'Variación vs Histórico (%)'}
    )
    fig.update_layout(
        paper_bgcolor='#0f1117',
        plot_bgcolor='#1a1d2e',
        font_color='#ffffff'
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs=False)

def generar_reporte(ventas_actual, ventas_anterior, variacion,
                    df_categorias, df_top, df_bottom, df_regiones):

    grafico_categorias = generar_grafico_categorias(df_categorias)
    grafico_regiones = generar_grafico_regiones(df_regiones)

    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: #0f1117; color: #e2e8f0; font-family: 'DM Sans', sans-serif; padding: 40px; }
            .header { border-bottom: 1px solid #2d3748; padding-bottom: 24px; margin-bottom: 32px; }
            .header h1 { font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }
            .header p { color: #718096; font-size: 14px; margin-top: 4px; }
            .kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 40px; }
            .kpi-card { background: #1a1d2e; border-radius: 8px; padding: 24px; border: 1px solid #2d3748; }
            .kpi-card .label { font-size: 12px; color: #718096; text-transform: uppercase; letter-spacing: 1px; }
            .kpi-card .value { font-family: 'IBM Plex Mono', monospace; font-size: 28px; font-weight: 600; margin-top: 8px; }
            .kpi-card .delta { font-family: 'IBM Plex Mono', monospace; font-size: 14px; margin-top: 4px; }
            .positive { color: #00C896; }
            .negative { color: #FF4B4B; }
            .section { margin-bottom: 40px; }
            .section h2 { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; }
            table { width: 100%; border-collapse: collapse; font-size: 14px; }
            th { text-align: left; padding: 10px 16px; background: #1a1d2e; color: #718096; font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
            td { padding: 10px 16px; border-bottom: 1px solid #1a1d2e; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }
            tr:hover td { background: #1a1d2e; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Retail Weekly Report</h1>
            <p>Semana del 03 Sep — 09 Sep 2017 · Generado el {{ fecha_generacion }}</p>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="label">Ventas Semana Actual</div>
                <div class="value">${{ ventas_actual }}</div>
            </div>
            <div class="kpi-card">
                <div class="label">Ventas Semana Anterior</div>
                <div class="value">${{ ventas_anterior }}</div>
            </div>
            <div class="kpi-card">
                <div class="label">Variación Semanal</div>
                <div class="value {{ 'positive' if variacion > 0 else 'negative' }}">{{ variacion }}%</div>
            </div>
        </div>

        <div class="section">
            <h2>Ventas por Categoría</h2>
            {{ grafico_categorias }}
        </div>

        <div class="section">
            <h2>Regiones vs Promedio Histórico</h2>
            {{ grafico_regiones }}
        </div>

        <div class="section">
            <h2>Top 10 Productos</h2>
            <table>
                <tr><th>Producto</th><th>Categoría</th><th>Ventas</th></tr>
                {% for _, row in df_top.iterrows() %}
                <tr>
                    <td>{{ row.product_name }}</td>
                    <td>{{ row.category }}</td>
                    <td>${{ "{:,.2f}".format(row.total_ventas) }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div class="section">
            <h2>Bottom 10 Productos</h2>
            <table>
                <tr><th>Producto</th><th>Categoría</th><th>Ventas</th></tr>
                {% for _, row in df_bottom.iterrows() %}
                <tr>
                    <td>{{ row.product_name }}</td>
                    <td>{{ row.category }}</td>
                    <td>${{ "{:,.2f}".format(row.total_ventas) }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

    </body>
    </html>
    """

    template = Template(template_str)
    html = template.render(
        fecha_generacion=datetime.now().strftime("%d %b %Y, %H:%M"),
        ventas_actual=f"{ventas_actual:,.2f}",
        ventas_anterior=f"{ventas_anterior:,.2f}",
        variacion=variacion,
        grafico_categorias=grafico_categorias,
        grafico_regiones=grafico_regiones,
        df_top=df_top,
        df_bottom=df_bottom
    )

    with open("outputs/report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte generado: outputs/report.html")