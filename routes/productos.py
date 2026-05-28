from flask import Blueprint, render_template
from flask import request, redirect, flash, session
from database.conexion import obtener_conexion
from utils.auth import login_required
from flask import jsonify
import os

from werkzeug.utils import secure_filename

productos = Blueprint("productos", __name__)

# PAGINA PRINCIPAL
@productos.route("/")
@login_required
def inicio():

    conexion = obtener_conexion()

    
    cursor = conexion.cursor()

    buscar = request.args.get("buscar", "")
    orden = request.args.get("orden", "")
    stock = request.args.get("stock", "")

    #CONSULTA BASE
    consulta = """
                SELECT * FROM Productos
                WHERE activo = 1
                AND nombre LIKE ?
            """
                                      
    
    #Filtrar stock Bajo
    if stock == "bajo":
        consulta += " AND cantidad <= 5"

    #Filtrar stock Alto
    elif stock == "alto":
        consulta += " AND cantidad > 5"

    #Filtar por precio
    if orden == "nombre_asc":
        consulta += " ORDER BY nombre ASC"

    elif orden == "precio_mayor":
        consulta += " ORDER BY precio DESC"
        
    elif orden == "precio_menor":
        consulta += " ORDER BY precio ASC"

    cursor.execute(consulta, (f"%{buscar}%",))
    
    
    productos = cursor.fetchall()


    #RESUMEN INVENTARIO

    cursor.execute("""
                SELECT
                   SUM(cantidad) AS total_unidades,
                   SUM(precio * cantidad) AS valor_total
                FROM Productos
                WHERE activo = 1
                """)
    
    resumen = cursor.fetchone()

    conexion.close()

    return render_template("index.html", 
                           productos=productos,
                           resumen=resumen
                        )


# GUARDAR PRODUCTO
@productos.route("/guardar-producto", methods=["POST"])
@login_required
def guardar_producto():

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]
    descripcion = request.form["descripcion"]
    imagen = request.files["imagen"]

    if imagen.filename == "":
        flash("⚠ Debes seleccionar una imagen.")
        return redirect("/")

    nombre_imagen = secure_filename(imagen.filename)
    ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
    imagen.save(ruta_imagen)

   
    #VALIDACIÓN DE CAMPOS
    if nombre == "" or precio == "" or cantidad == "" or descripcion == "":
        flash("⚠ Todos los campos son obligatorios.")
        return redirect("/")
    
    #CONVERTIR DATOS
    precio = float(precio)
    cantidad = int(cantidad)
  

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO Productos (nombre, precio, cantidad, descripcion, imagen)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, precio, cantidad, descripcion, nombre_imagen))

    conexion.commit()
    flash("✔Producto guardado correctamente.")

    conexion.close()
    
    return redirect("/")

@productos.route("/desactivar-producto/<int:id>", methods=["POST"])
@login_required
def desactivar_producto(id):

    conexion = obtener_conexion()


    cursor = conexion.cursor()

    cursor.execute("""
                        UPDATE Productos
                        SET activo = 0
                        WHERE Id = ?
                        """, (id,))

    conexion.commit()
    flash("Producto desactivado correctamente.")
    conexion.close()

    return redirect("/")


@productos.route("/papelera")
@login_required
def papelera():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Productos WHERE activo = 0")

    productos_desactivados = cursor.fetchall()

    conexion.close()

    return render_template("papelera.html", productos=productos_desactivados)



@productos.route("/reactivar-producto/<int:id>", methods=['POST'])
@login_required
def reactivar_producto(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
                        UPDATE Productos
                        SET activo = 1
                        WHERE id = ?
                    """, (id,))

    conexion.commit()
    print("Producto reactivado correctamente.")

    conexion.close()

    return redirect("/papelera")


@productos.route("/eliminar-producto/<int:id>", methods=['POST'])
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
                        DELETE FROM Productos
                        WHERE id = ?
                    """, (id,))

    conexion.commit()
    flash("✔Producto eliminado correctamente.")

    conexion.close()

    return redirect("/papelera")


@productos.route("/editar-producto/<int:id>")
@login_required
def editar_producto(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
                SELECT * FROM Productos
                WHERE id = ?
            """, (id,)
            )
    
    producto = cursor.fetchone()
    conexion.close()
    

    return render_template(
                        "editar_producto.html",
                        producto=producto
                    )

@productos.route("/actualizar-producto/<int:id>", methods=['POST'])
@login_required
def actualizar_producto(id):

    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    cantidad = int(request.form["cantidad"])
    descripcion = request.form["descripcion"]
    
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
                        UPDATE Productos
                        SET nombre = ?, 
                            precio = ?, 
                            cantidad = ?, 
                            descripcion = ?
                        WHERE id = ?
                    """, (nombre, precio, cantidad, descripcion, id))
    
    conexion.commit()
    flash("Producto actualizado correctamente. ")

    return redirect("/")

# API REST PARA OBTENER PRODUCTOS EN FORMATO JSON
@productos.route("/api/productos")
@login_required
def api_productos():

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
                SELECT * FROM Productos
                WHERE activo = 1
             """)
        
        productos_db = cursor.fetchall()

        conexion.close()

        productos_json = []

        for producto in productos_db:

            productos_json.append({
                "id": producto[0],
                "nombre": producto[1],
                "precio": producto[2],
                "cantidad": producto[3],
                "descripcion": producto[4],
                "imagen": producto[7]
            })

        return jsonify(productos_json)
