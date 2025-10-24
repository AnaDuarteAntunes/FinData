# routes.py
from flask import render_template, redirect, url_for, flash, request
from . import db, bcrypt
from .models import User, Transaction
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, TransactionForm
from datetime import datetime

def init_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('dashboard'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Cuenta creada correctamente', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Login fallido. Verifica email y contraseña', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # ------------------- PÁGINAS PRINCIPALES -------------------

    @app.route('/dashboard')
    @login_required
    def dashboard():
        expenses = Transaction.query.filter_by(user_id=current_user.id, type='expense').all()
        incomes = Transaction.query.filter_by(user_id=current_user.id, type='income').all()

        total_expenses = sum(t.amount for t in expenses)
        total_incomes = sum(t.amount for t in incomes)
        balance = total_incomes - total_expenses

        return render_template(
            'dashboard.html',
            total_expenses=total_expenses,
            total_incomes=total_incomes,
            balance=balance
        )

    @app.route('/expenses', methods=['GET', 'POST'])
    @login_required
    def expenses():
        form = TransactionForm()
        #if form.validate_on_submit() and form.type.data == 'expense':
        if form.validate_on_submit():
            transaction = Transaction(
                date=form.date.data,
                amount=form.amount.data,
                type='expense',
                category=form.category.data,
                description=form.description.data,
                user_id=current_user.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash('Gasto añadido correctamente.', 'success')
            return redirect(url_for('expenses'))
        
        expenses_list = Transaction.query.filter_by(user_id=current_user.id, type='expense').order_by(Transaction.date.desc()).all()
        incomes_list = Transaction.query.filter_by(user_id=current_user.id, type='income').all()

        total_expenses = sum(t.amount for t in expenses_list)
        total_incomes = sum(t.amount for t in incomes_list)
        balance = total_incomes - total_expenses

        return render_template('expenses.html',
                           form=form,
                           expenses=expenses_list,
                           total_expenses=total_expenses,
                           total_incomes=total_incomes,
                           balance=balance)

    @app.route('/incomes', methods=['GET', 'POST'])
    @login_required
    def incomes():
        form = TransactionForm()
        #if form.validate_on_submit() and form.type.data == 'income':
        if form.validate_on_submit():
            transaction = Transaction(
                date=form.date.data,
                amount=form.amount.data,
                type='income',
                category='General',  # valor por defecto
                description=form.description.data,
                user_id=current_user.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash('Ingreso añadido correctamente.', 'success')
            return redirect(url_for('incomes'))
    
        incomes_list = Transaction.query.filter_by(user_id=current_user.id, type='income').order_by(Transaction.date.desc()).all()
        expenses_list = Transaction.query.filter_by(user_id=current_user.id, type='expense').all()

        total_expenses = sum(t.amount for t in expenses_list)
        total_incomes = sum(t.amount for t in incomes_list)
        balance = total_incomes - total_expenses

        return render_template(
            'incomes.html',
            form=form,
            incomes=incomes_list,
            total_incomes=total_incomes,
            total_expenses=total_expenses,
            balance=balance
        )

    @app.route('/transactions')
    @login_required
    def transactions():
        # Obtener parámetros de filtros de la URL
        filter_type = request.args.get('type')
        filter_category = request.args.get('category')
        filter_date_from = request.args.get('date_from')
        filter_date_to = request.args.get('date_to')
        
        # Query base: todas las transacciones del usuario actual
        query = Transaction.query.filter_by(user_id=current_user.id)
        
        # Aplicar filtros si existen
        if filter_type:
            query = query.filter_by(type=filter_type)
        
        if filter_category:
            query = query.filter_by(category=filter_category)
        
        if filter_date_from:
            from datetime import datetime
            date_from = datetime.strptime(filter_date_from, '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= date_from)
        
        if filter_date_to:
            from datetime import datetime
            date_to = datetime.strptime(filter_date_to, '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= date_to)
        
        # Ejecutar query con orden descendente por fecha
        transactions = query.order_by(Transaction.date.desc()).all()
        
        return render_template('transactions.html', transactions=transactions)
