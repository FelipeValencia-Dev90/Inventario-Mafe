import pyodbc

conexion = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
    'DATABASE=InventarioAVA;'
    'Trusted_Connection=yes;'
)

print("Conexión exitosa 🚀")

