# routes.py
from flask import render_template, redirect, url_for, flash, request
from . import db, bcrypt
from .models import User, Transaction
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, TransactionForm
from datetime import datetime
from sqlalchemy import extract, func
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

        current_year = datetime.now().year
        previous_year = current_year - 1

        expenses = Transaction.query.filter_by(user_id=current_user.id, type='expense').all()
        incomes = Transaction.query.filter_by(user_id=current_user.id, type='income').all()

        total_expenses = sum(t.amount for t in expenses)
        total_incomes = sum(t.amount for t in incomes)
        balance = total_incomes - total_expenses

        # --- DATOS DEL AÑO ACTUAL ---
        expenses_current = Transaction.query.filter_by(
            user_id=current_user.id, 
            type='expense'
        ).filter(
            extract('year', Transaction.date) == current_year
        ).all()
        
        incomes_current = Transaction.query.filter_by(
            user_id=current_user.id, 
            type='income'
        ).filter(
            extract('year', Transaction.date) == current_year
        ).all()

        total_expenses = sum(t.amount for t in expenses_current)
        total_incomes = sum(t.amount for t in incomes_current)
        balance = total_incomes - total_expenses
        
        # Tasa de ahorro del año actual
        saving_rate_current = (balance / total_incomes * 100) if total_incomes > 0 else 0
        
        # --- DATOS DEL AÑO ANTERIOR (para comparación) ---
        incomes_previous = Transaction.query.filter_by(
            user_id=current_user.id, 
            type='income'
        ).filter(
            extract('year', Transaction.date) == previous_year
        ).all()
        
        expenses_previous = Transaction.query.filter_by(
            user_id=current_user.id, 
            type='expense'
        ).filter(
            extract('year', Transaction.date) == previous_year
        ).all()
        
        total_incomes_previous = sum(t.amount for t in incomes_previous)
        total_expenses_previous = sum(t.amount for t in expenses_previous)
        balance_previous = total_incomes_previous - total_expenses_previous
        
        # Tasa de ahorro del año anterior
        saving_rate_previous = (balance_previous / total_incomes_previous * 100) if total_incomes_previous > 0 else 0
        
        # Diferencia entre años
        saving_rate_diff = saving_rate_current - saving_rate_previous
        
        # --- Datos para gráfico de área (por mes del año actual) ---
        
        # Ingresos por mes
        income_by_month = db.session.query(
            extract('month', Transaction.date).label('month'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == 'income',
            extract('year', Transaction.date) == current_year
        ).group_by('month').all()
        
        # Gastos por mes
        expense_by_month = db.session.query(
            extract('month', Transaction.date).label('month'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == 'expense',
            extract('year', Transaction.date) == current_year
        ).group_by('month').all()
        
        # Convertir a diccionarios para fácil acceso
        income_dict = {int(m): float(t) for m, t in income_by_month}
        expense_dict = {int(m): float(t) for m, t in expense_by_month}
        
        # Crear listas con todos los 12 meses (poner 0 si no hay datos)
        monthly_incomes = [income_dict.get(m, 0) for m in range(1, 13)]
        monthly_expenses = [expense_dict.get(m, 0) for m in range(1, 13)]
        
        # --- Datos para gráfico circular (gastos por categoría del año actual) ---
        expenses_by_category = db.session.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == 'expense',
            extract('year', Transaction.date) == current_year
        ).group_by(Transaction.category).all()
        
        category_labels = [cat for cat, _ in expenses_by_category]
        category_amounts = [float(total) for _, total in expenses_by_category]

        return render_template(
            'dashboard.html',
            total_expenses=total_expenses,
            total_incomes=total_incomes,
            balance=balance,
            saving_rate_current=saving_rate_current,
            saving_rate_previous=saving_rate_previous,
            saving_rate_diff=saving_rate_diff,
            monthly_incomes=monthly_incomes,
            monthly_expenses=monthly_expenses,
            category_labels=category_labels,
            category_amounts=category_amounts,
            current_year=current_year
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
