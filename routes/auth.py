from flask import Blueprint, render_template
from flask import request, redirect, flash, session

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
        AND contraseña = ?
    """, (correo, contraseña))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario:

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