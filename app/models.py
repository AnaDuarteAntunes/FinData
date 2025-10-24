from . import db
from flask_login import UserMixin #me da los métodos necesarios para usar Flask-Login
from datetime import datetime

# Modelo de usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relación con transacciones- permite acceder a todas las transacciones de un usuario
    transactions = db.relationship('Transaction', backref='user', lazy=True)

# Modelo de transacción (ingreso o gasto)
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)  # ingresos positivos, gastos negativos
    type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
