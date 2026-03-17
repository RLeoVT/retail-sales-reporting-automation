import sqlite3
from src.queries import get_ventas_semana, get_top_cat, get_top_productos, get_bottom_productos, get_avg_region
from src.transform import calcular_variacion, calcular_variacion_categoria
from src.report import generar_reporte
from src.mailer import enviar_reporte


conn = sqlite3.connect("db/retail.db")

df_ventas = get_ventas_semana(conn)
ventas_actual, ventas_anterior, variacion = calcular_variacion(df_ventas)
# print(f"Ventas semana actual: ${ventas_actual:,.2f}")
# print(f"Ventas semana anterior: ${ventas_anterior:,.2f}")
# print(f"Variación: {variacion}%")

df_categorias = get_top_cat(conn)
df_variacion_categoria = calcular_variacion_categoria(df_categorias)
# print(df_variacion_categoria)

df_top = get_top_productos(conn)
df_bottom = get_bottom_productos(conn)
# print(df_top)
# print(df_bottom)

df_variacion_region = get_avg_region(conn)
# print(df_variacion_region)

generar_reporte(
    ventas_actual, ventas_anterior, variacion,
    df_variacion_categoria, df_top, df_bottom, df_variacion_region
)   

enviar_reporte()

conn.close()