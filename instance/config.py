import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_super_secreta')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///findata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
