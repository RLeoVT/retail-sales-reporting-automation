import pandas as pd
import sqlite3

df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")
#print(df.head())

df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
#print(df.head())

conn = sqlite3.connect("db/retail.db")
df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')
df.to_sql("orders", conn, if_exists="replace", index=False)

# Verificación real
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM orders")
rows_in_db = cursor.fetchone()[0]

conn.close()

print(f"Filas en CSV: {len(df)}")
print(f"Filas en base de datos: {rows_in_db}")