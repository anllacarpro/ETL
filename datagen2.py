import sqlite3
import numpy as np
from datetime import datetime, timedelta
import random

# Nombre de la base de datos
db_path = 'comercio_ventas.db'

# Conectar a SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear 200 comercios adicionales
np.random.seed(1)  # Fijar semilla para reproducibilidad
comercios = [
    (f"2055{str(i).zfill(5)}", f"C{str(i).zfill(3)}", f"Comercio {i}", "Dirección Y", "987654321",
     f"correo{i}@example.com", random.choice(["Lima", "Arequipa", "Cusco", "Trujillo", "Piura"]),
     random.choice(["Miraflores", "San Isidro", "Centro", "Los Olivos", "Surco"]),
     "Provincia X", "Departamento X", random.choice(["Minorista", "Mayorista"]),
     random.choice(["Alimentos", "Tecnología", "Moda", "Salud", "Hogar"]),
     round(np.random.uniform(50000, 200000), 2), 
     (datetime.now() - timedelta(days=np.random.randint(0, 3650))).strftime("%Y-%m-%d"),
     np.random.randint(5, 100), 
     random.choice(["Diaria", "Semanal", "Mensual"]), 
     random.choice(["Bronce", "Plata", "Oro"]))
    for i in range(6, 206)  # IDs de comercios de 6 a 205
]

# Insertar los nuevos comercios en la base de datos
cursor.executemany("""
INSERT INTO Comercio (RUC, codigo_comercio, nombre_comercio, direccion, telefono, email, ciudad,
                      distrito, provincia, departamento, tipo_comercio, sector, ingresos_anuales,
                      fecha_apertura, numero_empleados, frecuencia_transacciones, nivel_lealtad)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", comercios)

# Recuperar los nuevos IDs de comercio
comercio_ids = [row[0] for row in cursor.execute("SELECT id_comercio FROM Comercio").fetchall()]

# Crear productos para los nuevos comercios
productos = [
    (comercio_id, f"Producto {chr(65+i%26)}", random.choice(["Electrónica", "Ropa", "Alimentos", "Muebles"]), 
     round(np.random.uniform(10, 500), 2))
    for comercio_id in comercio_ids
    for i in range(5)  # Cinco productos por comercio
]

# Insertar los productos en la base de datos
cursor.executemany("""
INSERT INTO Producto (id_comercio, nombre_producto, categoria, precio_unitario)
VALUES (?, ?, ?, ?)
""", productos)

# Recuperar todos los IDs de producto
producto_ids = [row[0] for row in cursor.execute("SELECT id_producto FROM Producto").fetchall()]

# Generar transacciones para cada comercio (varias transacciones por comercio)
transacciones = []
detalle_transacciones = []
transaction_count = 0

for comercio_id in comercio_ids:
    # Cada comercio tendrá entre 10 y 50 transacciones
    num_transacciones = random.randint(10, 50)
    for _ in range(num_transacciones):
        transaction_count += 1
        id_producto = random.choice(producto_ids)
        fecha_transaccion = datetime.now() - timedelta(days=np.random.randint(0, 365))
        tipo_operacion = "Venta"
        id_operacion = f"{comercio_id}_{transaction_count}"
        estado = random.choice(["En proceso", "Completado", "Rechazado"])
        monto = round(np.random.uniform(5, 2000), 2)
        moneda = "Soles"
        motivo_venta_observada = random.choice(["", "Sin observaciones", "Observado"])
        numero_serie_terminal = f"{np.random.randint(100000, 999999)}"
        codigo_autorizacion = f"{np.random.randint(100000, 999999)}"
        numero_referencia = f"{random.randint(100000000000, 999999999999)}"
        numero_lote = f"{np.random.randint(1000, 9999)}"
        monto_dcc = round(np.random.uniform(0, 50), 2)
        dcc = random.choice(["SI", "NO"])
        numero_tarjeta = f"{np.random.randint(4000, 4999)}******{np.random.randint(1000, 9999)}"
        origen_tarjeta = random.choice(["Nacional", "Internacional"])
        tipo_tarjeta = random.choice(["Débito", "Crédito"])
        marca_tarjeta = random.choice(["Visa", "MasterCard", "Amex"])
        tipo_captura = random.choice(["CHIP", "QR", "Magstripe", "Manual"])
        banco_emisor = random.choice(["BCP", "Interbank", "Scotiabank", "BBVA"])
        numero_cuenta = f"{random.randint(1000000000, 9999999999)}"
        banco_pagador = random.choice(["BCP", "Interbank", "Scotiabank", "BBVA"])
        numero_cuotas = np.random.randint(0, 12)
        transaccion_cuotas_sin_interes = random.choice(["SI", "NO"])
        nombre_programa = random.choice(["", "Paga Rápido", "Cashback Program", "Descuento Especial"])

        transacciones.append((comercio_id, fecha_transaccion, tipo_operacion, id_operacion, estado, monto, moneda, 
                              id_producto, motivo_venta_observada, numero_serie_terminal, codigo_autorizacion, 
                              numero_referencia, numero_lote, monto_dcc, dcc, numero_tarjeta, origen_tarjeta, tipo_tarjeta, 
                              marca_tarjeta, tipo_captura, banco_emisor, numero_cuenta, banco_pagador, numero_cuotas, 
                              transaccion_cuotas_sin_interes, nombre_programa))
        
        # Detalle de la transacción
        importe_descuento = round(np.random.uniform(0, 100), 2)
        cashback = random.choice(["SI", "NO"])
        monto_cashback = round(np.random.uniform(0, 20), 2)
        comision_cuota_sin_interes = round(np.random.uniform(0, 10), 2)
        paga_rapido = random.choice(["SI", "NO"])
        qr = random.choice(["SI", "NO"])
        importe_propina = round(np.random.uniform(0, 15), 2)
        
        detalle_transacciones.append((transaction_count, importe_descuento, cashback, monto_cashback, 
                                      comision_cuota_sin_interes, paga_rapido, qr, importe_propina))

# Insertar las transacciones en la base de datos
cursor.executemany("""
INSERT INTO Transaccion (id_comercio, fecha_transaccion, tipo_operacion, id_operacion, estado, monto, moneda, 
                         id_producto, motivo_venta_observada, numero_serie_terminal, codigo_autorizacion, 
                         numero_referencia, numero_lote, monto_dcc, dcc, numero_tarjeta, origen_tarjeta, tipo_tarjeta, 
                         marca_tarjeta, tipo_captura, banco_emisor, numero_cuenta, banco_pagador, numero_cuotas, 
                         transaccion_cuotas_sin_interes, nombre_programa)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", transacciones)

# Insertar detalles de las transacciones en la base de datos
cursor.executemany("""
INSERT INTO Detalle_Transaccion (id_transaccion, importe_descuento, cashback, monto_cashback, 
                                 comision_cuota_sin_interes, paga_rapido, qr, importe_propina)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", detalle_transacciones)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Comercios, transacciones y detalles adicionales insertados con éxito.")