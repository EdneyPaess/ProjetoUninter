from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Inicializar a aplicação Flask
app = Flask(__name__)

# Configurações vindas do arquivo config.py
app.config.from_object('config.Config')


# Inicializar o banco de dados
db = SQLAlchemy(app)
jwt = JWTManager(app)

from routes import *

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)
