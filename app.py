from flask import Flask
from flask_jwt_extended import JWTManager

from routes.productos import productos
from routes.auth import auth
from flasgger import Swagger

from datetime import timedelta


app = Flask(__name__)


app.secret_key = "InventarioAVA"
app.config["JWT_SECRET_KEY"] = "super-secret-key"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(productos)

@app.errorhandler(404)
def pagino_no_encontrada(error):

    return {
        "success": False,
        "mensaje": "Ruta no encontrada"
    }, 404


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
        
app.run(debug=True)