import os
import pyodbc

def obtener_conexion():
    url_nube = os.environ.get('DATABASE_URL')
    
    if url_nube:
        import psycopg2
        return psycopg2.connect(url_nube)    
            
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
        'DATABASE=InventarioAVA;'
        'Trusted_Connection=yes;'
    )