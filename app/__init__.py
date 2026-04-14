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

    # CAMBIO 1: Cargar configuracion segun entorno
    # Si existe instance/config.py (local), lo usa.
    # Si no existe (produccion), usa variables de entorno de Render.
    try:
        app.config.from_object('instance.config.Config')
    except ModuleNotFoundError:
        # Configuracion para produccion en Render:
        # Tomamos la URL de la base de datos desde la variable de entorno.
        database_url = os.environ.get('DATABASE_URL')

        # Si DATABASE_URL no existe, detenemos la app en lugar de caer en SQLite.
        # Asi evitamos bugs silenciosos en produccion.
        if not database_url:
            raise RuntimeError("DATABASE_URL no esta configurada en Render")

        # CAMBIO 2: Render a veces entrega la URL como postgres://
        # pero SQLAlchemy espera postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        # Configuracion principal de Flask y SQLAlchemy en produccion.
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-super-secreta-por-defecto')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Refuerzo extra:
    # Si por cualquier motivo la URI siguiera viniendo con postgres://,
    # la corregimos aqui tambien.
    if (
        app.config.get('SQLALCHEMY_DATABASE_URI')
        and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://")
    ):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            "postgres://", "postgresql://", 1
        )

    # Inicializamos extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configuracion de LoginManager
    login_manager.login_view = 'login'          # Ruta de login para @login_required
    login_manager.login_message_category = 'info'  # Categoria del mensaje flash

    # Definir user_loader para Flask-Login:
    # Flask-Login usa esta funcion para reconstruir el usuario autenticado
    # a partir del user_id guardado en la sesion.
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar modelos, crear tablas y cargar rutas dentro del contexto de la app
    with app.app_context():
        from . import models
        db.create_all()  # Crea las tablas si no existen

        # Importar y registrar todas las rutas
        from .routes import init_routes
        init_routes(app)

    return app