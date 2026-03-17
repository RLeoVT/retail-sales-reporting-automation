import sqlite3
import pandas as pd

# Ventas totales semana actual vs semana anterior 
# ¿Cuánto vendimos esta semana y cuánto variamos respecto a la semana pasada?
def get_ventas_semana(conn):
    query = """
        SELECT
            CASE
                WHEN order_date BETWEEN '2017-09-03' AND '2017-09-09' THEN 'semana_actual'
                WHEN order_date BETWEEN '2017-08-27' AND '2017-09-02' THEN 'semana_anterior'
            END AS periodo,
            ROUND(SUM(sales), 2) AS total_ventas
        FROM orders
        WHERE order_date BETWEEN '2017-08-27' AND '2017-09-09'
        GROUP BY periodo
        HAVING periodo IS NOT NULL
        ORDER BY periodo DESC
    """
    return pd.read_sql(query, conn)

# Ventas por categoría
# ¿Qué categorías están creciendo y cuáles cayendo semana a semana?
def get_top_cat(conn):
    query = """
        SELECT
            category,
            CASE
                WHEN order_date BETWEEN '2017-09-03' AND '2017-09-09' THEN 'semana_actual'
                WHEN order_date BETWEEN '2017-08-27' AND '2017-09-02' THEN 'semana_anterior'
            END AS periodo,
            ROUND(SUM(sales), 2) AS total_ventas
        FROM orders
        WHERE order_date BETWEEN '2017-08-27' AND '2017-09-09'
        GROUP BY category, periodo
        HAVING periodo IS NOT NULL
        ORDER BY category, periodo DESC
    """
    return pd.read_sql(query, conn)

# Top 10 y Bottom 10 productos
# ¿Qué productos generan más revenue y cuáles están underperforming?
def get_top_productos(conn):
    query = """
        SELECT
            product_name,
            category,
            ROUND(SUM(sales), 2) AS total_ventas
        FROM orders
        WHERE order_date BETWEEN '2017-09-03' AND '2017-09-09'
        GROUP BY product_name, category
        ORDER BY total_ventas DESC
        LIMIT 10
    """
    return pd.read_sql(query, conn)

def get_bottom_productos(conn):
    query = """
        SELECT
            product_name,
            category,
            ROUND(SUM(sales), 2) AS total_ventas
        FROM orders
        WHERE order_date BETWEEN '2017-09-03' AND '2017-09-09'
        GROUP BY product_name, category
        ORDER BY total_ventas ASC
        LIMIT 10
    """
    return pd.read_sql(query, conn)

# Desempeño por región
# ¿Qué regiones están por encima o por debajo de su promedio histórico?
def get_avg_region(conn):
    query = """
        WITH promedio_historico AS (
            SELECT
                region,
                ROUND(AVG(weekly_sales), 2) AS promedio_semanal
            FROM (
                SELECT
                    region,
                    strftime('%Y-%W', order_date) AS semana,
                    ROUND(SUM(sales), 2) AS weekly_sales
                FROM orders
                WHERE order_date < '2017-09-03'
                GROUP BY region, semana
            )
            GROUP BY region
        )
        SELECT
            o.region,
            ROUND(SUM(o.sales), 2) AS ventas_semana_actual,
            ph.promedio_semanal,
            ROUND((SUM(o.sales) - ph.promedio_semanal) / ph.promedio_semanal * 100, 2) AS variacion_vs_historico
        FROM orders o
        JOIN promedio_historico ph ON o.region = ph.region
        WHERE o.order_date BETWEEN '2017-09-03' AND '2017-09-09'
        GROUP BY o.region, ph.promedio_semanal
        ORDER BY variacion_vs_historico DESC
    """
    return pd.read_sql(query, conn)