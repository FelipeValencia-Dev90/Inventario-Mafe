import pyodbc

def obtener_conexion():

    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
        'DATABASE=InventarioAVA;'
        'Trusted_Connection=yes;'
    )

    return conexion