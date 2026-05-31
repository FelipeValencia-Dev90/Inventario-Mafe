import sys
import os

# le enseña a Python a mirar una carpeta hacia atrás
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion

import matplotlib.pyplot as plt

import pandas as pd


conexion = obtener_conexion()

consulta = """
        SELECT nombre, precio, cantidad
        FROM Productos
        WHERE activo = 1
"""

df = pd.read_sql(consulta, conexion)

df["alerta_stock"] = df["cantidad"] < 30

df["ventas_diarias"] = [5, 20, 10, 8, 7, 3, 11, 5, 9, 2]
df["dias_restantes"] = df["cantidad"] / df["ventas_diarias"]

print("\n📊 PREDICCIÓN DE STOCK📊\n")

print(df[[
    "nombre",
    "cantidad",
    "ventas_diarias",
    "dias_restantes"
]])

plt.figure(figsize=(10,5))

plt.bar(df["nombre"], df["cantidad"])

plt.xticks(rotation=45)

plt.title("Stock de productos")

plt.xlabel("Productos")

plt.ylabel("Cantidad")

plt.tight_layout()

plt.show()

conexion.close()