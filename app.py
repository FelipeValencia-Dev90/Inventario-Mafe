from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from routes.productos import productos
from routes.auth import auth
from flasgger import Swagger

from datetime import timedelta

from utils.errors import configurar_errores


app = Flask(__name__)

load_dotenv()

configurar_errores(app)


app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(productos)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Inventario AVA API",
        "description": "API profesional de inventario",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header usando Bearer"
        }
    }
}

Swagger(app, config=swagger_config, template=template)


if __name__ == "__main__":
    app.run(debug=True)
