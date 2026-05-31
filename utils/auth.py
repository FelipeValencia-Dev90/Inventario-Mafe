from flask import session, redirect
from functools import wraps
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def login_required(funcion):

    @wraps(funcion)
    def proteger_ruta(*args, **kwargs):

        if "usuario" not in session:
            return redirect("/login")

        return funcion(*args, **kwargs)

    return proteger_ruta


def admin_required(funcion):

    @wraps(funcion)
    def proteger_admin(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()

        if claims["rol"] != "admin":

            return {
                "success": False,
                "mensaje": "Acceso denegado"
            }, 403

        return funcion(*args, **kwargs)

    return proteger_admin