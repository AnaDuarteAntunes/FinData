# analysis.py
import pandas as pd
from datetime import datetime
from sqlalchemy import extract, func
from .models import Transaction
from . import db
import matplotlib
matplotlib.use('Agg')  # Importante: usar backend no-GUI
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import numpy as np

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

def generate_charts(user_id, year=None):
    """
    Genera gráficos con Matplotlib y los retorna como imágenes base64.
    
    Args:
        user_id: ID del usuario
        year: Año a analizar (None = año actual)
    
    Returns:
        Diccionario con imágenes en base64
    """
    if year is None:
        year = datetime.now().year
        
    # Configurar estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Obtener transacciones del año
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        extract('year', Transaction.date) == year
    ).all()
    
    if not transactions:
        return {
            'histogram': None,
            'trend': None,
            'heatmap': None
        }
    
    # Crear DataFrame
    df = pd.DataFrame([{
        'date': t.date,
        'amount': float(t.amount),
        'type': t.type,
        'category': t.category,
        'month': t.date.month
    } for t in transactions])
    
    charts = {}
    
    # --- GRÁFICO 1: Histograma Comparativa de Años ---

    try:
        
        # Asegurar que la columna 'date' sea datetime
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            print("DEBUG - Convirtiendo df['date'] a datetime...")
            df['date'] = pd.to_datetime(df['date'])
        
        # Crear la columna month
        df['month'] = df['date'].dt.month

        # Obtener gastos del año actual
        current_expenses = df[df['type'] == 'expense'].copy()    
        current_expenses['month'] = current_expenses['date'].dt.month
        current_monthly = current_expenses.groupby('month')['amount'].sum()

        # Obtener gastos del año anterior
        previous_year = year - 1
        previous_transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            extract('year', Transaction.date) == previous_year,
            Transaction.type == 'expense'
        ).all()
                
        if previous_transactions:
            previous_df = pd.DataFrame([
                {
                    'date': t.date,
                    'amount': float(t.amount),
                    'month': t.date.month
                }
                for t in previous_transactions
            ])
            previous_monthly = previous_df.groupby('month')['amount'].sum()
        else:
            previous_monthly = pd.Series(dtype=float)
        
        # Crear arrays para todos los meses (1-12)
        months = list(range(1, 13))
        current_amounts = [current_monthly.get(m, 0) for m in months]
        previous_amounts = [previous_monthly.get(m, 0) for m in months]
        
        # Si no hay datos, no generar gráfico
        if sum(current_amounts) == 0 and sum(previous_amounts) == 0:
            charts['histogram'] = None
        else:
            # Crear gráfico de barras agrupadas
            fig, ax = plt.subplots(figsize=(12, 6))
            x = np.arange(len(months))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, previous_amounts, width, 
                        label=f'{previous_year}', color='#d1d3e0', alpha=0.8)
            bars2 = ax.bar(x + width/2, current_amounts, width, 
                        label=f'{year}', color='#e74a3b', alpha=0.9)
            
            ax.set_xlabel('Mes', fontsize=12)
            ax.set_ylabel('Gastos (€)', fontsize=12)
            ax.set_title(f'Comparativa de Gastos Mensuales: {year} vs {previous_year}', 
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
            ax.legend(loc='upper left')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Formato de moneda en eje Y
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}€'))
            
            # Convertir a base64
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            charts['histogram'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
    except Exception as e:
        print(f"Error generando gráfico comparativo: {e}")
        charts['histogram'] = None
    
    # --- GRÁFICO 2: Línea de tendencia de ahorro mensual ---
    try:
        # Calcular balance por mes
        monthly_balance = []
        for month in range(1, 13):
            month_data = df[df['month'] == month]
            income = month_data[month_data['type'] == 'income']['amount'].sum()
            expense = month_data[month_data['type'] == 'expense']['amount'].sum()
            balance = income - expense
            monthly_balance.append(balance)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        months_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        ax.plot(months_labels, monthly_balance, marker='o', linewidth=2, 
                markersize=8, color='#4e73df')
        ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax.fill_between(range(12), monthly_balance, alpha=0.3)
        
        ax.set_xlabel('Mes', fontsize=12)
        ax.set_ylabel('Balance (€)', fontsize=12)
        ax.set_title(f'Tendencia de Ahorro Mensual - {year}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Convertir a base64
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        charts['trend'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
    except Exception as e:
        print(f"Error generando tendencia: {e}")
        charts['trend'] = None
    
    # --- GRÁFICO 3: Mapa de calor (Categorías vs Meses) ---
    try:
        expenses_df = df[df['type'] == 'expense'].copy()
        
        if len(expenses_df) > 0:
            expenses_df['date'] = pd.to_datetime(expenses_df['date'], errors='coerce')
            expenses_df['month'] = expenses_df['date'].dt.month # Extraer el mes de la columna 'date'

            # Crear pivot table
            pivot = expenses_df.pivot_table(
                values='amount', 
                index='category', 
                columns='month', 
                aggfunc='sum', 
                fill_value=0
            )
            
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
                       cbar_kws={'label': 'Cantidad (€)'}, ax=ax, linewidths=0.5)
            
            ax.set_xlabel('Mes', fontsize=12)
            ax.set_ylabel('Categoría', fontsize=12)
            ax.set_title(f'Mapa de Calor: Gastos por Categoría y Mes - {year}', 
                        fontsize=14, fontweight='bold')
            
            # Etiquetas de meses            
            meses_en_datos = pivot.columns.tolist() 
            etiquetas_meses = {
                1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
            }

            # etiquetas solo para los meses que existen en los datos
            etiquetas = [etiquetas_meses.get(mes, str(mes)) for mes in meses_en_datos]
            ax.set_xticklabels(etiquetas)
            
            # También ajustar las etiquetas del eje Y si es necesario
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

            # Convertir a base64
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            charts['heatmap'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
        else:
            charts['heatmap'] = None
    except Exception as e:
        print(f"Error generando mapa de calor: {e}")
        charts['heatmap'] = None
    
    return charts