import pyodbc

conexion = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
    'DATABASE=InventarioAVA;'
    'Trusted_Connection=yes;'
)

cursor = conexion.cursor()  

cursor.execute("""
INSERT INTO Productos (nombre, precio, cantidad, descripcion)
VALUES ('TV', 2500000, 4, 'Smart TV')
""")

conexion.commit()  