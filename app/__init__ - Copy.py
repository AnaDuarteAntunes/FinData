from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Inicializamos extensiones
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.Config')

    # Inicializamos extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'login'

    # Contexto de la app para poder crear tablas
    with app.app_context():
        from . import models
        db.create_all()  # crea las tablas si no existen
        from . import routes

    return app
