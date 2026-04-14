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

    # CAMBIO 1: Prioridad a variables de entorno.
    # En Render debe usarse DATABASE_URL.
    # Si no existe DATABASE_URL, usamos instance/config.py para entorno local.
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Configuracion para produccion (Render)

        # Render puede entregar postgres:// pero SQLAlchemy espera postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-super-secreta-por-defecto')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    else:
        # Configuracion local: usa SQLite desde instance/config.py
        app.config.from_object('instance.config.Config')

    # Inicializamos extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configuracion de LoginManager
    login_manager.login_view = 'login'  # Ruta de login para @login_required
    login_manager.login_message_category = 'info'  # Categoria del mensaje flash

    # Definir user_loader para Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar rutas y crear tablas dentro del contexto de la app
    with app.app_context():
        from . import models
        db.create_all()  # Crea las tablas si no existen

        # Importar la funcion que registra todas las rutas
        from .routes import init_routes
        init_routes(app)  # Registrar rutas en la app

    return app