from werkzeug.security import generate_password_hash
from database.conexion import obtener_conexion

conexion = obtener_conexion()

cursor = conexion.cursor()

nombre = "felipe"
correo = "felipe10@gmail.com"

contraseña = generate_password_hash("12345")

cursor.execute("""
    INSERT INTO Usuarios (nombre, correo, contraseña)
    VALUES (?, ?, ?)
""", (nombre, correo, contraseña))

conexion.commit()

print("✅ Usuario creado correctamente")

conexion.close()