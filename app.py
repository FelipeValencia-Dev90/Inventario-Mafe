from flask import Flask
from routes.productos import productos
from routes.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(productos)
app.secret_key = "InventarioAVA"
        
app.run(debug=True)