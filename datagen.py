import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generación de datos ficticios para la tabla Comercio
comercio_data = {
    "id_comercio": range(1, 6),
    "RUC": ["20555530090", "20177710021", "20666620032", "20777730043", "20888840054"],
    "codigo_comercio": ["C001", "C002", "C003", "C004", "C005"],
    "nombre_comercio": ["Comercio A", "Comercio B", "Comercio C", "Comercio D", "Comercio E"],
    "direccion": ["Dir A", "Dir B", "Dir C", "Dir D", "Dir E"],
    "telefono": ["123456789", "987654321", "123123123", "321321321", "456456456"],
    "email": ["a@example.com", "b@example.com", "c@example.com", "d@example.com", "e@example.com"],
    "fecha_registro": pd.date_range(start="2023-01-01", periods=5).strftime("%Y-%m-%d").tolist()
}
comercio_df = pd.DataFrame(comercio_data)

# Generación de datos ficticios para la tabla Producto
producto_data = {
    "id_producto": range(1, 11),
    "id_comercio": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    "nombre_producto": ["Producto A1", "Producto A2", "Producto B1", "Producto B2", "Producto C1", 
                        "Producto C2", "Producto D1", "Producto D2", "Producto E1", "Producto E2"],
    "categoria": ["Categoría 1", "Categoría 2", "Categoría 1", "Categoría 2", "Categoría 1", 
                  "Categoría 2", "Categoría 1", "Categoría 2", "Categoría 1", "Categoría 2"],
    "precio_unitario": np.random.uniform(10, 100, 10).round(2)
}
producto_df = pd.DataFrame(producto_data)

# Generación de datos ficticios para la tabla Transaccion
num_transacciones = 20
transaccion_data = {
    "id_transaccion": range(1, num_transacciones + 1),
    "id_comercio": np.random.choice(comercio_df["id_comercio"], num_transacciones),
    "fecha_transaccion": [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(num_transacciones)],
    "tipo_operacion": ["Venta"] * num_transacciones,
    "id_operacion": [f"OP{str(i).zfill(6)}" for i in range(1, num_transacciones + 1)],
    "estado": np.random.choice(["En proceso", "Completado", "Rechazado"], num_transacciones),
    "monto": np.random.uniform(5, 200, num_transacciones).round(2),
    "moneda": ["Soles"] * num_transacciones,
    "id_producto": np.random.choice(producto_df["id_producto"], num_transacciones),
    "motivo_venta_observada": np.random.choice(["", "Sin observaciones", "Observado"], num_transacciones)
}
transaccion_df = pd.DataFrame(transaccion_data)
transaccion_df["estado"] = np.random.choice(transaccion_data["estado"], num_transacciones)
transaccion_df["motivo_venta_observada"] = np.random.choice(transaccion_data["motivo_venta_observada"], num_transacciones)

# Generación de datos ficticios para la tabla Detalle_Transaccion
detalle_transaccion_data = {
    "id_detalle_transaccion": range(1, num_transacciones + 1),
    "id_transaccion": transaccion_df["id_transaccion"],
    "importe_descuento": np.random.uniform(0, 20, num_transacciones).round(2),
    "cashback": np.random.choice([0, 1], num_transacciones),
    "monto_cashback": np.random.uniform(0, 10, num_transacciones).round(2),
    "importe_propina": np.random.uniform(0, 15, num_transacciones).round(2)
}
detalle_transaccion_df = pd.DataFrame(detalle_transaccion_data)

# Guardar los datos en archivos CSV para simular la base de datos y un archivo Excel para las transacciones
comercio_df.to_csv("Comercio.csv", index=False)
producto_df.to_csv("roducto.csv", index=False)
transaccion_df.to_csv("Transaccion.csv", index=False)
detalle_transaccion_df.to_csv("Detalle_Transaccion.csv", index=False)

# Guardar la transacción en un Excel para emular el archivo de datos de ventas
with pd.ExcelWriter("Transacciones_Excel.xlsx") as writer:
    transaccion_df.to_excel(writer, sheet_name="Transacciones", index=False)
    detalle_transaccion_df.to_excel(writer, sheet_name="Detalle_Transacciones", index=False)

("Comercio.csv", "Producto.csv", "Transaccion.csv", "Detalle_Transaccion.csv", "Transacciones_Excel.xlsx")
