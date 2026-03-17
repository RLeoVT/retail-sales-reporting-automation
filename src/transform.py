import pandas as pd

def calcular_variacion(df_ventas_semana):
    ventas_actual = df_ventas_semana.loc[df_ventas_semana['periodo'] == 'semana_actual', 'total_ventas'].values[0]
    ventas_anterior = df_ventas_semana.loc[df_ventas_semana['periodo'] == 'semana_anterior', 'total_ventas'].values[0]
    variacion = round(((ventas_actual - ventas_anterior) / ventas_anterior) * 100, 2)

    return ventas_actual, ventas_anterior, variacion


def calcular_variacion_categoria(df_ventas_categoria):
    actual = df_ventas_categoria[df_ventas_categoria['periodo'] == 'semana_actual'].set_index('category')['total_ventas']
    anterior = df_ventas_categoria[df_ventas_categoria['periodo'] == 'semana_anterior'].set_index('category')['total_ventas']
    
    resultado = pd.DataFrame({
        'ventas_actual': actual,
        'ventas_anterior': anterior,
        'variacion_pct': round(((actual - anterior) / anterior) * 100, 2)
    }).reset_index()
    
    return resultado