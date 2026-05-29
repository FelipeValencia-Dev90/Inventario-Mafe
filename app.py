from flask import Flask
from routes.productos import productos
from routes.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(productos)
app.secret_key = "InventarioAVA"

@app.errorhandler(404)
def pagino_no_encontrada(error):

    return {
        "success": False,
        "mensaje": "Ruta no encontrada"
    }, 404
        
app.run(debug=True)