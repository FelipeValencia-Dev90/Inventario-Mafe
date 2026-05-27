from flask import session, redirect
from functools import wraps

def login_required(funcion):

    @wraps(funcion)
    def proteger_ruta(*args, **kwargs):

        if "usuario" not in session:
            return redirect("/login")

        return funcion(*args, **kwargs)

    return proteger_ruta