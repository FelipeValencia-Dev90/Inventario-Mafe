from flask import Blueprint, render_template
from flask import request, redirect, flash, session
from database.conexion import obtener_conexion
from utils.auth import login_required
from flask import jsonify
from flask_jwt_extended import jwt_required
from utils.auth import admin_required
from utils.logger import logger
import os

import subprocess
from datetime import datetime


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

    # ELIMINAR ESPACIOS EN BLANCO AL INICIO Y FINAL DEL NOMBRE
    nombre = nombre.strip()
    descripcion = descripcion.strip()

    if imagen.filename == "":
        flash("⚠ Debes seleccionar una imagen.")
        return redirect("/")

    nombre_imagen = secure_filename(imagen.filename)

    extensiones_permitidas = ["jpg", "jpeg", "png"]
    extension = nombre_imagen.split(".")[-1].lower()

    if extension not in extensiones_permitidas:
        flash("⚠ Formato de imagen no permitido.")
        return redirect("/")


    ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
    imagen.save(ruta_imagen)

   
    #VALIDACIÓN DE CAMPOS
    if nombre == "" or precio == "" or cantidad == "" or descripcion == "":
        flash("⚠ Todos los campos son obligatorios.")
        return redirect("/")
    
    if len(nombre) < 3:
        flash("⚠ El nombre debe tener al menos 3 caracteres.")
        return redirect("/")
    
    if len(descripcion) < 10:
        flash("⚠ La descripción debe tener al menos 10 caracteres.")
        return redirect("/")
    
    try:
        precio = float(precio)
        cantidad = int(cantidad)

    except ValueError:
        flash("⚠ Precio o cantidad invalidos.")
        return redirect("/")



    #CONVERTIR DATOS
    precio = float(precio)
    cantidad = int(cantidad)

    if precio <= 0:
        flash("⚠ El precio debe ser mayor a 0.")
        return redirect("/")
    
    if cantidad < 0:
        flash("⚠ La cantidad no puede ser negativa.")
        return redirect("/")
  

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM Productos
        WHERE nombre = ?
    """, (nombre,))

    producto_existente = cursor.fetchone()

    if producto_existente:
        flash("⚠ Ya existe un producto con ese nombre.")
        conexion.close()

        return redirect("/")

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

@productos.route("/vender-producto/<int:id>", methods=["POST"])
@login_required
def vender_producto(id):

    try:

        cantidad_vendida = int(request.form["cantidad"])

        # VALIDAR CANTIDAD NEGATIVA
        if cantidad_vendida <= 0:

            flash("⚠ La cantidad vendida debe ser mayor a 0")
            return redirect("/")

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT cantidad
            FROM Productos
            WHERE id = ?
        """, (id,))

        producto = cursor.fetchone()

        if not producto:

            flash("❌ Producto no encontrado")
            return redirect("/")

        stock_actual = producto[0]

        if cantidad_vendida > stock_actual:

            flash("⚠ Stock insuficiente")

            conexion.close()

            return redirect("/")

        nuevo_stock = stock_actual - cantidad_vendida

        cursor.execute("""
            UPDATE Productos
            SET cantidad = ?
            WHERE id = ?
        """, (nuevo_stock, id))

        cursor.execute("""
            INSERT INTO Ventas(producto_id, cantidad)
            VALUES(?, ?)
        """, (id, cantidad_vendida))

        conexion.commit()

        conexion.close()

        logger.info(
            f"Venta Realizada | Producto ID: {id} | Cantidad: {cantidad_vendida}"
        )

        flash("✅ Venta registrada")

    except Exception as error:

        logger.error(f"Error en la venta: {error}")

        flash("🚨 Ocurrió un error en la venta")

    return redirect("/")

# API REST PARA OBTENER PRODUCTOS EN FORMATO JSON
@productos.route("/api/productos")
@admin_required
@jwt_required()
def api_productos():
        
        """
        Listar productos
        ---
        tags:
            - Productos

        security:
            - Bearer: []
        responses:
            200:
                description: Lista de productos
        """
            
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


@productos.route("/api/user/productos")
@jwt_required()
def api_user_productos():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre, precio, cantidad
        FROM Productos
        WHERE activo = 1
    """)

    productos_db = cursor.fetchall()

    conexion.close()

    productos_json = []

    for producto in productos_db:

        productos_json.append({
            "nombre": producto[0],
            "precio": producto[1],
            "cantidad": producto[2]
        })

    return jsonify(productos_json), 200

@productos.route("/api/productos", methods=["POST"])
@login_required
def crear_producto_api():

    try:

        datos = request.get_json()

        nombre = datos["nombre"]
        precio = datos["precio"]
        cantidad = datos["cantidad"]
        descripcion = datos["descripcion"]


        #VALIDACION DE CAMPOS

        if not nombre:
             return jsonify({
                  "success": False,
                  "mensaje": "El nombre es obligatorio"
             }), 400
        
        if not precio:
            return jsonify({
                    "success": False,
                    "mensaje": "El precio es obligatorio"
                }), 400
        
        if not cantidad:
             return jsonify({
                  "success": False,
                  "mensaje": "la cantidad es obligatoria"
             }), 400

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO Productos
            (nombre, precio, cantidad, descripcion)
            VALUES (?, ?, ?, ?)
        """, (nombre, precio, cantidad, descripcion))

        conexion.commit()

        conexion.close()

        return jsonify({
            "success": True,
            "mensaje": "Producto creado correctamente"
        }), 201
    
    except Exception as e:
         
        return jsonify({
            "success": False,
            "mensaje": str(e)
        }), 500

@productos.route("/api/productos/<int:id>", methods=["PUT"])
@login_required
def editar_producto_api(id):
    
        datos = request.get_json()

        nombre = datos["nombre"]
        precio = datos["precio"]
        cantidad = datos["cantidad"]
        descripcion = datos["descripcion"]

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE Productos
            SET nombre = ?, precio = ?, cantidad = ?, descripcion = ?
            WHERE id = ?
        """, (nombre, precio, cantidad, descripcion, id))

        conexion.commit()

        conexion.close()

        return jsonify({
            "mensaje": "Producto actualizado correctamente"
        }), 200

@productos.route("/api/productos/<int:id>", methods=["DELETE"])
@login_required
def eliminar_producto_api(id):
     
        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM Productos
            WHERE id = ?
        """, (id,))

        conexion.commit()

        conexion.close()

        return jsonify({
            "mensaje": "Producto eliminado correctamente"
        }), 200

@productos.route("/backup")
@login_required
def crear_backup():
    try:
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"inventario_{fecha}.bak"
        
        # 1. Ruta temporal en el disco C accesible para SQL Server
        ruta_temporal_sql = f"C:\\temp_backups\\{nombre_archivo}"

        # 2. Comando usando Driver 17 (agregamos -C por seguridad)
        comando_lista = [
            "sqlcmd",
            "-S", "DESKTOP-Q681RM2\\SQLEXPRESS",
            "-Q", f"BACKUP DATABASE InventarioAVA TO DISK='{ruta_temporal_sql}'",
            "-C"
        ]

        resultado = subprocess.run(comando_lista, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            raise Exception(resultado.stderr or resultado.stdout)

        # 3. Ruta final de tu proyecto donde tú quieres ver el archivo
        ruta_destino_proyecto = os.path.abspath(os.path.join("backups", nombre_archivo))

        # 4. Con la ayuda de Python, movemos el archivo de la carpeta temporal a tu app
        if os.path.exists(ruta_temporal_sql):
            import shutil
            shutil.move(ruta_temporal_sql, ruta_destino_proyecto)
            flash(f"✅ Respaldo creado correctamente en tu proyecto: {nombre_archivo}")
        else:
            raise Exception("El archivo no se encontró en la carpeta temporal.")

    except Exception as e:
        flash(f"❌ Error creando respaldo: {e}")

    return redirect("/")