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

    # Configuración de LoginManager
    login_manager.login_view = 'login'  # ruta de login para @login_required
    login_manager.login_message_category = 'info'  # categoría flash

    # Definir user_loader para Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar rutas y crear tablas dentro del contexto de la app
    with app.app_context():
        from . import models
        db.create_all()  # crea las tablas si no existen

        # Importar la función que registra todas las rutas
        from .routes import init_routes
        init_routes(app)  # registrar rutas en la app

    return app

