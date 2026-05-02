from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# PAGINA PRINCIPAL
@app.route("/")
def inicio():

    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
        'DATABASE=InventarioAVA;'
        'Trusted_Connection=yes;'
    )

    
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Productos WHERE activo = 1")

    productos = cursor.fetchall()

    conexion.close()

    return render_template("index.html", productos=productos)


# GUARDAR PRODUCTO
@app.route("/guardar-producto", methods=["POST"])
def guardar_producto():

    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    cantidad = int(request.form["cantidad"])
    descripcion = request.form["descripcion"]

    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-Q681RM2\\SQLEXPRESS;'
        'DATABASE=InventarioAVA;'
        'Trusted_Connection=yes;'
    )

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO Productos (nombre, precio, cantidad, descripcion)
        VALUES (?, ?, ?, ?)
    """, (nombre, precio, cantidad, descripcion))

    conexion.commit()
    conexion.close()

    return redirect("/")


app.run(debug=True)