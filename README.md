# 💰 FinData - Gestor de Finanzas Personales

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)


> Aplicación web para la gestión y análisis de finanzas personales con visualización de datos y análisis estadísticos.

<br>

Proyecto desarrollado como estudiante de Desarrollo de Aplicaciones Multiplataforma. Creado para uso personal y como parte de mi portafolio de desarrollo.
<br>
<br>

---

## 🎯 Motivación del Proyecto

Este proyecto nace de una necesidad personal: **tener control total sobre mis finanzas de forma visual e intuitiva**.

Como estudiante de DAM, quería crear algo que:

- ✅ Resuelva un problema real en mi día a día
- 📚 Demuestre mis habilidades en desarrollo full-stack
- 🎨 Sirva como pieza destacada en mi portafolio profesional
- 💡 Me permita aprender y aplicar tecnologías modernas

**FinData** es mi solución personal que combina funcionalidad práctica con diseño profesional.

---

<br>

## 📋 Descripción

**FinData** es una aplicación web moderna que permite a los usuarios:

- ✅ Registrar ingresos y gastos de forma sencilla
- 📊 Visualizar datos mediante gráficos dinámicos e interactivos
- 🔍 Filtrar y analizar transacciones por categoría, tipo y fecha
- 📈 Calcular automáticamente balances y tasas de ahorro
- 🔐 Gestión segura de usuarios con autenticación

---

<br>

![Image](https://github.com/user-attachments/assets/9dc80f48-4e0d-44ec-89d8-567e909c1c14)

<br>

---

## 🚀 Características Principales

### 📊 Dashboard Interactivo
- Tarjetas resumen con totales de ingresos, gastos y balance
- Cálculo automático de tasa de ahorro
- Gráficos de evolución temporal (Chart.js)
- Distribución de gastos por categoría

### 💸 Gestión de Transacciones
- Formularios intuitivos para registrar ingresos y gastos
- Categorización de gastos (Alimentación, Transporte, Vivienda, etc.)
- Historial completo con búsqueda y ordenación (DataTables)
- Filtros avanzados por tipo, categoría y rango de fechas

### 🔐 Autenticación y Seguridad
- Sistema de registro y login seguro
- Contraseñas hasheadas con bcrypt
- Sesiones de usuario con Flask-Login
- Datos privados por usuario

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones de usuario
- **Flask-Bcrypt** - Encriptación de contraseñas
- **WTForms** - Validación de formularios

### Frontend
- **HTML5 / CSS3** - Estructura y estilos
- **Bootstrap 4** - Framework CSS responsive
- **Jinja2** - Motor de plantillas
- **SB Admin 2** - Template de administración
- **Chart.js** - Gráficos interactivos
- **DataTables** - Tablas avanzadas con búsqueda/filtrado

### Base de Datos
- **SQLite** - Base de datos local

### Análisis de Datos (Próximamente)
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Visualización estadística
- **Power BI** - Dashboards avanzados

---

## 📦 Instalación

### Requisitos Previos
- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/findata.git
cd findata
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
- **Windows:**
```bash
venv\Scripts\activate
```
- **Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar base de datos**
```bash
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

6. **Ejecutar la aplicación**
```bash
python run.py
```

7. **Acceder a la aplicación**
Abre tu navegador en: `http://localhost:5000`

---

## 📁 Estructura del Proyecto

```
findata/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── models.py            # Modelos de base de datos
│   ├── forms.py             # Formularios WTForms
│   ├── routes.py            # Rutas y controladores
│   ├── static/              # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── css/
│   │   ├── js/
│   │   ├── vendor/
│   │   └── img/
│   └── templates/           # Templates HTML (Jinja2)
│       ├── index.html       # Template base
│       ├── dashboard.html   # Dashboard principal
│       ├── incomes.html     # Gestión de ingresos
│       ├── expenses.html    # Gestión de gastos
│       ├── transactions.html # Historial completo
│       ├── login.html       # Página de login
│       └── register.html    # Página de registro
├── instance/               # Base de datos SQLite
├── run.py                   # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

---

## 🎯 Uso de la Aplicación

### 1. Registro e Inicio de Sesión
1. Accede a `/register` para crear una cuenta
2. Inicia sesión en `/login` con tus credenciales

### 2. Registrar Transacciones
- **Ingresos:** Ve a la sección "Ingresos" y añade tus entradas de dinero
- **Gastos:** Ve a la sección "Gastos" y registra tus gastos por categoría

### 3. Visualizar Datos
- **Dashboard:** Visualiza resúmenes, gráficos y estadísticas
- **Transacciones:** Consulta todo el historial con filtros avanzados

### 4. Análisis
- Utiliza los filtros para analizar gastos por periodo o categoría
- Monitoriza tu tasa de ahorro en tiempo real

---

## 🔐 Modelos de Datos

### Usuario (User)
```python
- id: Integer (PK)
- email: String (unique)
- password_hash: String
- created_at: DateTime
```

### Transacción (Transaction)
```python
- id: Integer (PK)
- user_id: Integer (FK)
- date: Date
- amount: Decimal(10,2)
- type: String ('income' / 'expense')
- category: String
- description: String
- created_at: DateTime
```

---

## 🚧 Roadmap

### ✅ Fase 1 - Funcionalidad Básica (Completada)
- [x] Sistema de autenticación
- [x] CRUD de transacciones
- [x] Dashboard con estadísticas básicas
- [x] Filtrado de transacciones

### 🔄 Fase 2 - Análisis Avanzado (En progreso)
- [x] Integración con Pandas para análisis de datos
- [x] Gráficos avanzados con Matplotlib
- [x] Exportación de datos a CSV/Excel
- [ ] Reportes mensuales/anuales

### 📅 Fase 3 - Características Premium (Planificado)
- [ ] Integración con Power BI
- [ ] Predicciones de gastos con Machine Learning
- [ ] Presupuestos y alertas
- [ ] Categorías personalizadas
- [ ] Objetivos de ahorro

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---


## 📸 Capturas de Pantalla

### Dashboard
<img width="1897" height="865" alt="findata_dashboard" src="https://github.com/user-attachments/assets/b1e44b42-1d91-4b73-9018-10ea7ce21ebe" />


### Gestión de Gastos
<img width="1865" height="874" alt="findata_gastos" src="https://github.com/user-attachments/assets/5e1004b2-ede8-4ca9-8154-ef71d210206e" />

### Historial de Transacciones
<img width="1893" height="877" alt="findata_tabla" src="https://github.com/user-attachments/assets/c65b01d1-02cc-4006-af75-5a5e155dc729" />

---

## 🙏 Agradecimientos

- [SB Admin 2](https://startbootstrap.com/theme/sb-admin-2) - Template de administración
- [Chart.js](https://www.chartjs.org/) - Biblioteca de gráficos
- [DataTables](https://datatables.net/) - Plugin de tablas interactivas
- [Flask](https://flask.palletsprojects.com/) - Framework web

---

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un [issue](https://github.com/tu-usuario/findata/issues) en GitHub.

---

<div align="center">
  <p>© 2025 FinData - Todos los derechos reservados</p>
</div>
