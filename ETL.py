import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite
db_path = 'comercio_ventas.db'
conn = sqlite3.connect(db_path)

# Extracción: Leer datos de las tablas de SQLite
comercio_df = pd.read_sql_query("SELECT * FROM Comercio", conn)
producto_df = pd.read_sql_query("SELECT * FROM Producto", conn)
transaccion_df = pd.read_sql_query("SELECT * FROM Transaccion", conn)
detalle_transaccion_df = pd.read_sql_query("SELECT * FROM Detalle_Transaccion", conn)

# Cerrar la conexión a la base de datos
conn.close()

# Transformación: Realizar algunas transformaciones en los datos
# 1. Unir las tablas Transaccion y Detalle_Transaccion para obtener detalles completos de cada transacción
transaccion_completa = pd.merge(transaccion_df, detalle_transaccion_df, left_on='id_transaccion', right_on='id_transaccion')

# 2. Agregar detalles del comercio y producto para cada transacción
transaccion_completa = pd.merge(transaccion_completa, comercio_df, left_on='id_comercio', right_on='id_comercio')
transaccion_completa = pd.merge(transaccion_completa, producto_df, left_on='id_producto', right_on='id_producto', suffixes=('_comercio', '_producto'))

# 3. Calcular campos adicionales, por ejemplo:
# - Día del mes de la transacción
transaccion_completa['DayOfMonth'] = pd.to_datetime(transaccion_completa['fecha_transaccion']).dt.day
# - Hora del día de la transacción
transaccion_completa['HourOfDay'] = pd.to_datetime(transaccion_completa['fecha_transaccion']).dt.hour
print(transaccion_completa.head())
# - Total con descuento aplicado
transaccion_completa['monto_final'] = transaccion_completa['monto'] - transaccion_completa['importe_descuento']
# - Indicar si la transacción es de alto valor (mayor a 1000)
transaccion_completa['transaccion_alto_valor'] = transaccion_completa['monto'] > 1000
# - Crear una columna con el año de la transacción para análisis temporal
transaccion_completa['año_transaccion'] = pd.to_datetime(transaccion_completa['fecha_transaccion']).dt.year

# Carga: Guardar el resultado en un archivo CSV o analizarlo directamente
transaccion_completa.to_csv("reporte_transacciones_completo.csv", index=False)

print("ETL completado. El reporte de transacciones completas ha sido guardado como 'reporte_transacciones_completo.csv'.")
