import os
import pyodbc

def obtener_conexion():
    url_nube = os.environ.get('DATABASE_URL')
    
    if url_nube:
        import psycopg2
        conexion = psycopg2.connect(url_nube)
        
        # --- AUTOMIGRACIÓN EN LA NUBE ---
        # Cada vez que se conecte en Render, verificará y creará las tablas de forma interna
        cursor = conexion.cursor()
        script_tablas = """
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        try:
            cursor.execute(script_tablas)
            conexion.commit()
        except Exception as e:
            print(f"Error al auto-crear tablas: {e}")
        finally:
            cursor.close()
            
        return conexion
    else:
        # Conexión para tu computadora local con SQL Server
        conexion_local = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
            'DATABASE=InventarioAVA;'
            'Trusted_Connection=yes;'
        )
        return conexion_local