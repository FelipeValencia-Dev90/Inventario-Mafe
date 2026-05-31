from flask import Blueprint, render_template
from flask import request, redirect, flash, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import jsonify



from database.conexion import obtener_conexion

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():


    if request.method == "GET":
        return render_template("login.html")

    correo = request.form["correo"]
    contraseña = request.form["contraseña"]

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM Usuarios
        WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario and check_password_hash(usuario[3], contraseña):

        session["usuario"] = usuario[1]

        flash("✔ Bienvenido al sistema AVA")

        return redirect("/")

    else:

        flash("⚠ Correo o contraseña incorrectos")

        return redirect("/login")
    
@auth.route("/logout")
def logout():

    session.pop("usuario", None)

    flash("✔ Has cerrado sesión correctamente.")
    return redirect("/login")


@auth.route("/api/login", methods=["POST"])
def api_login():

    datos = request.get_json()

    correo = datos.get("correo")
    contraseña = datos.get("contraseña")

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM Usuarios
        WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario and check_password_hash(usuario[3], contraseña):

        token = create_access_token(
            identity=str(usuario[1]),
            additional_claims={
                "rol": usuario[4]
            }
        )


        refresh_token = create_refresh_token(
            identity=str(usuario[1]),
            additional_claims={
                "rol": usuario[4]
            }
        )


        return jsonify({
            "success": True,
            "access_token": token,
            "refresh_token": refresh_token
        }), 200
    

    return jsonify({
        "success": False,
        "mensaje": "Credenciales incorrectas"
    }), 401

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    usuario = get_jwt_identity()

    nuevo_token = create_access_token(identity=usuario)

    return jsonify({
        "access_token": nuevo_token
    }), 200