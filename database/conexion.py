import os
import pyodbc

def obtener_conexion():
    url_nube = os.environ.get('DATABASE_URL')
    
    if url_nube:
        import psycopg2
        conexion = psycopg2.connect(url_nube)
        cursor = conexion.cursor()
        
        script_tablas = """
        DROP TABLE IF EXISTS historial_movimiento CASCADE;
        DROP TABLE IF EXISTS ventas CASCADE;
        DROP TABLE IF EXISTS productos CASCADE;
        DROP TABLE IF EXISTS usuarios CASCADE;

        CREATE TABLE usuarios (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );

        CREATE TABLE productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            cantidad INT NOT NULL,
            descripcion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo INT DEFAULT 1,
            imagen VARCHAR(255)
        );
        
        CREATE TABLE ventas (
            id SERIAL PRIMARY KEY,
            producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
            cantidad INT NOT NULL,
            total DECIMAL(10, 2) NOT NULL,
            fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE historial_movimiento (
            id SERIAL PRIMARY KEY,
            producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
            accion VARCHAR(100) NOT NULL,
            cantidad INT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        conexion_local = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
            'DATABASE=InventarioAVA;'
            'Trusted_Connection=yes;'
        )
        return conexion_local