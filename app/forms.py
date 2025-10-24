from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional

# Formulario de registro
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

# Formulario de login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Formulario para transacción (ingreso/gasto)
class TransactionForm(FlaskForm):
    TYPE_CHOICES = [
        ('income', 'Ingreso'),
        ('expense', 'Gasto')
    ]

    CATEGORY_CHOICES = [
        ('Alimentación', 'Alimentación'),
        ('Transporte', 'Transporte'),
        ('Vivienda', 'Vivienda'),
        ('Ocio', 'Ocio'),
        ('Educación', 'Educación'),
        ('Salud', 'Salud'),
        ('Ropa', 'Ropa'),
        ('Servicios', 'Servicios'),
        ('Mascotas', 'Mascotas'),
        ('Otros', 'Otros')
    ]

    date = DateField('Fecha', validators=[DataRequired()])
    amount = DecimalField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    #type = SelectField('Tipo de Transacción', choices=TYPE_CHOICES, default='income', validators=[DataRequired()])
    category = SelectField('Categoría (solo para gastos)', choices=CATEGORY_CHOICES, validators=[Optional()])
    description = TextAreaField('Descripción', validators=[Optional()])
    submit = SubmitField('Guardar')

