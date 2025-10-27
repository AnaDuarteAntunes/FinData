# analysis.py
import pandas as pd
from datetime import datetime
from sqlalchemy import extract, func
from .models import Transaction
from . import db


def get_monthly_summary(user_id, year=None):
    """
    Retorna un DataFrame con resumen mensual de ingresos, gastos y balance.
    
    Args:
        user_id: ID del usuario
        year: Año a analizar (None = año actual)
    
    Returns:
        DataFrame con columnas: Mes, Ingresos, Gastos, Balance
    """
    if year is None:
        year = datetime.now().year
    
    # Consulta de ingresos por mes
    incomes = db.session.query(
        extract('month', Transaction.date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'income',
        extract('year', Transaction.date) == year
    ).group_by('month').all()
    
    # Consulta de gastos por mes
    expenses = db.session.query(
        extract('month', Transaction.date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'expense',
        extract('year', Transaction.date) == year
    ).group_by('month').all()
    
    # Convertir a diccionarios
    income_dict = {int(m): float(t) for m, t in incomes}
    expense_dict = {int(m): float(t) for m, t in expenses}
    
    # Crear DataFrame con todos los 12 meses
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    data = []
    for i in range(1, 13):
        income = income_dict.get(i, 0)
        expense = expense_dict.get(i, 0)
        balance = income - expense
        data.append({
            'Mes': months[i-1],
            'Ingresos': round(income, 2),
            'Gastos': round(expense, 2),
            'Balance': round(balance, 2)
        })
    
    df = pd.DataFrame(data)
    return df


def get_category_breakdown(user_id, year=None):
    """
    Retorna un DataFrame con el desglose de gastos por categoría.
    
    Args:
        user_id: ID del usuario
        year: Año a analizar (None = año actual)
    
    Returns:
        DataFrame con columnas: Categoría, Total, Porcentaje
    """
    if year is None:
        year = datetime.now().year
    
    # Consulta de gastos por categoría
    expenses = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'expense',
        extract('year', Transaction.date) == year
    ).group_by(Transaction.category).all()
    
    if not expenses:
        return pd.DataFrame(columns=['Categoría', 'Total', 'Porcentaje'])
    
    # Crear DataFrame
    data = []
    total_expenses = sum(float(t) for _, t in expenses)
    
    for category, amount in expenses:
        percentage = (float(amount) / total_expenses * 100) if total_expenses > 0 else 0
        data.append({
            'Categoría': category,
            'Total': round(float(amount), 2),
            'Porcentaje': round(percentage, 1)
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('Total', ascending=False)  # Ordenar de mayor a menor
    return df


def calculate_trends(user_id, months=6):
    """
    Calcula tendencias de los últimos N meses.
    
    Args:
        user_id: ID del usuario
        months: Número de meses a analizar (default: 6)
    
    Returns:
        Diccionario con métricas de tendencia
    """
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    
    # Fecha límite (hace N meses)
    end_date = datetime.now().date()
    start_date = end_date - relativedelta(months=months)
    
    # Obtener transacciones del período
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    if not transactions:
        return {
            'promedio_ingresos': 0,
            'promedio_gastos': 0,
            'promedio_balance': 0,
            'categoria_mas_gastada': 'N/A',
            'total_categoria_mas_gastada': 0,
            'meses_analizados': months
        }
    
    # Crear DataFrame
    df = pd.DataFrame([{
        'date': t.date,
        'amount': float(t.amount),
        'type': t.type,
        'category': t.category
    } for t in transactions])
    
    # Añadir columna de año-mes
    df['year_month'] = pd.to_datetime(df['date']).dt.to_period('M')
    
    # Calcular totales por mes
    monthly_incomes = df[df['type'] == 'income'].groupby('year_month')['amount'].sum()
    monthly_expenses = df[df['type'] == 'expense'].groupby('year_month')['amount'].sum()
    
    # Promedios
    avg_income = monthly_incomes.mean() if len(monthly_incomes) > 0 else 0
    avg_expense = monthly_expenses.mean() if len(monthly_expenses) > 0 else 0
    avg_balance = avg_income - avg_expense
    
    # Categoría más gastada
    expenses_df = df[df['type'] == 'expense']
    if len(expenses_df) > 0:
        category_totals = expenses_df.groupby('category')['amount'].sum()
        top_category = category_totals.idxmax()
        top_category_amount = category_totals.max()
    else:
        top_category = 'N/A'
        top_category_amount = 0
    
    return {
        'promedio_ingresos': round(avg_income, 2),
        'promedio_gastos': round(avg_expense, 2),
        'promedio_balance': round(avg_balance, 2),
        'categoria_mas_gastada': top_category,
        'total_categoria_mas_gastada': round(float(top_category_amount), 2),
        'meses_analizados': months
    }