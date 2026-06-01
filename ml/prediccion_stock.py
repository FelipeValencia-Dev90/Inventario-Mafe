import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

from database.conexion import obtener_conexion



conexion = obtener_conexion()

consulta = """
SELECT nombre, cantidad
FROM Productos
WHERE activo = 1
"""

df = pd.read_sql(consulta, conexion)

conexion.close()


# SIMULACIÓN VENTAS DIARIAS
df["ventas_diarias"] = [5, 20, 10, 8, 7, 3, 11, 5, 9, 2]


# VARIABLE X (ventas)
X = df[["ventas_diarias"]]

# VARIABLE Y (stock)
y = df["cantidad"]


# CREAR MODELO IA
modelo = LinearRegression()

# ENTRENAR IA
modelo.fit(X, y)


# PREDICCIÓN
prediccion = modelo.predict(X)

df["prediccion_stock"] = prediccion

df["riesgo"] = df["prediccion_stock"] < 40

colores = []

for riesgo in df["riesgo"]:

    if riesgo:
        colores.append("red")

    else:
        colores.append("green")


print("\n🤖 ANÁLISIS INTELIGENTE INVENTARIO 🤖\n")

print(df[[
    "nombre",
    "cantidad",
    "ventas_diarias",
    "prediccion_stock",
    "riesgo"
]])

plt.figure(figsize=(12, 6))

plt.bar(
    df["nombre"],
    df["prediccion_stock"],
    color=colores
)

plt.title("📊 Predicción Inteligente de Stock")

plt.xlabel("Productos")
plt.ylabel("Predicción Stock")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()