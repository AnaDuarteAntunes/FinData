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
    
    #  CAMBIO 1: Cargar configuraci贸n seg煤n entorno
    # Si existe instance/config.py (local), lo usa
    # Si no (producci贸n), usa variables de entorno
    try:
        app.config.from_object('instance.config.Config')
    except ModuleNotFoundError:
        # CONFIGURACIóN PRODUCCIóN (Render)
        database_url = os.environ.get('DATABASE_URL')

        if not database_url:
            raise RuntimeError("? DATABASE_URL no está configurada en Render")

        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-super-secreta-por-defecto')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #  CAMBIO 2: Fix para Render (PostgreSQL usa postgres:// pero SQLAlchemy necesita postgresql://)
    if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

    # Inicializamos extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configuraci贸n de LoginManager
    login_manager.login_view = 'login'  # ruta de login para @login_required
    login_manager.login_message_category = 'info'  # categor铆a flash

    # Definir user_loader para Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar rutas y crear tablas dentro del contexto de la app
    with app.app_context():
        from . import models
        db.create_all()  # crea las tablas si no existen

        # Importar la funci贸n que registra todas las rutas
        from .routes import init_routes
        init_routes(app)  # registrar rutas en la app

    return app

