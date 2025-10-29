# 💰 FinData - Gestor de Finanzas Personales

[![Demo en Vivo](https://img.shields.io/badge/Demo-En%20Vivo-success)](https://findata-r08l.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)


> Aplicación web para la gestión y análisis de finanzas personales con visualización de datos y análisis estadísticos.

<br>

FinData es un sistema de gestión financiera personal que permite registrar ingresos y gastos, visualizar estadísticas en tiempo real, y exportar reportes detallados. Diseñada con una interfaz intuitiva..

🎭 Modo Demo: Al acceder a la aplicación, podrás explorar todas las funcionalidades con datos ficticios precargados sin necesidad de registro<br>
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

## ✨ Características Principales

### 📊 Dashboard Interactivo
- Resumen de saldo actual, ingresos y gastos totales
- Gráficos de área para evolución temporal
- Gráfico circular de distribución por categorías
- Visualización de últimas 5 transacciones

### 💸 Gestión de Transacciones
- Registro de ingresos y gastos con categorización
- Filtros por tipo, categoría y rango de fechas
- Tabla interactiva con búsqueda y ordenamiento
- Eliminación de registros con confirmación

### 📈 Análisis Avanzado
- Gráficos estadísticos con Matplotlib y Seaborn
- Comparativa mensual de ingresos vs gastos
- Distribución porcentual por categorías
- Top 5 de gastos más frecuentes
- Filtrado por año para análisis histórico

### 📥 Exportación de Datos
- Descarga en formato CSV
- Descarga en formato Excel (XLSX)
- Filtros aplicables antes de exportar
- Datos listos para análisis externo

### 🔐 Sistema de Autenticación
- Registro de usuarios con validación
- Login seguro con contraseñas hasheadas (Bcrypt)
- Sesiones persistentes
- Modo demo sin necesidad de registro


---


## Dashboard

![Image](https://github.com/user-attachments/assets/0bf4aa79-9a22-467d-9e0b-2c9e7c7c20fd) <br>


## Gestiones
![Image](https://github.com/user-attachments/assets/4b552acb-f285-455f-8ea4-9be4ff910c9f)<br>

<br>

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones
- **Flask-Bcrypt** - Encriptación de contraseñas
- **Pandas** - Análisis de datos
- **Matplotlib + Seaborn** - Visualizaciones estadísticas

### Frontend
- **HTML5 / CSS3** - Estructura y estilos
- **Bootstrap 4** - Framework CSS responsive
- **SB Admin 2** - Plantilla de administración
- **Chart.js** - Gráficos interactivos
- **DataTables** - Tablas con funcionalidades avanzadas
- **Jinja2** - Motor de plantillas

### Base de Datos
- **SQLite** - Base de datos local
- **PostgreSQL** - Base de datos en producción

### Análisis de Datos 
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Visualización estadística
- **Power BI** - Dashboards avanzados (Próximamente)

### Despliegue
- **Render** - Hosting de aplicación y base de datos
- **Gunicorn** - Servidor WSGI para producción
- **GitHub Actions** - CI/CD automático

---

## 🚀 Demo en Vivo

Accede a la aplicación desplegada: **[https://findata-r08l.onrender.com](https://findata-r08l.onrender.com)**

Al entrar, verás automáticamente el dashboard con datos de demostración. Puedes:
- ✅ Navegar por todas las secciones
- ✅ Ver gráficos y estadísticas
- ✅ Probar filtros y búsquedas
- ✅ Exportar datos en CSV/Excel
- ⚠️ Los cambios no se guardarán (modo demo)

Si deseas crear tu propia cuenta con datos reales, haz clic en "Crear cuenta real" desde el banner superior.

## 📦 Instalación Local

### Requisitos Previos
- Python 3.11 o superior
- PostgreSQL (opcional, usa SQLite por defecto en local)
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
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu_clave_secreta_aqui
FLASK_ENV=development
DATABASE_URL=sqlite:///findata.db  # O tu URL de PostgreSQL
```

5. **Inicializar la base de datos**
```bash
flask db upgrade
```

6. **Ejecutar la aplicación**
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

---

## 🗂️ Estructura del Proyecto

```
findata/
├── app/
│   ├── __init__.py           # Configuración de Flask
│   ├── models.py             # Modelos de base de datos
│   ├── routes.py             # Rutas y lógica de vistas
│   ├── forms.py              # Formularios con WTForms
│   ├── analysis.py           # Funciones de análisis de datos
│   ├── templates/            # Plantillas HTML
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   ├── analytics.html
│   │   └── ...
│   └── static/               # Archivos CSS, JS e imágenes
│       ├── css/
│       ├── js/
│       └── vendor/
├── migrations/               # Migraciones de base de datos
├── run.py                    # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── render.yaml               # Configuración de Render
└── README.md                 # Este archivo
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
## 🔒 Seguridad

- Contraseñas encriptadas con Bcrypt
- Protección CSRF en formularios
- Validación de datos en servidor
- Sesiones seguras con Flask-Login
- Variables de entorno para datos sensibles

---
## 🚀 Despliegue en Render

Este proyecto está configurado para desplegarse automáticamente en Render:

1. Conecta tu repositorio de GitHub a Render
2. Configura las variables de entorno necesarias
3. Render detectará el `render.yaml` y desplegará automáticamente
4. Cada push a `main` actualizará la aplicación

---

## 🤝 Contribuciones
Este proyecto es parte de mi portafolio como estudiante de DAM. Si encuentras algún bug o tienes sugerencias de mejora, siéntete libre de abrir un issue o pull request.

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---


## 📸 Capturas de Pantalla

### Dashboard
<img width="1890" height="871" alt="findata_dashboard" src="https://github.com/user-attachments/assets/e951ff62-8699-4a24-9624-8e6027b8c8b7" />


### Análisis
<img width="1877" height="857" alt="findata_analisis1" src="https://github.com/user-attachments/assets/38ce290b-10d9-4520-adeb-f9de0ac962a0" />
<img width="1638" height="872" alt="findata_analisis2" src="https://github.com/user-attachments/assets/8e817641-f6a8-433e-abc0-5d69fdaeca5c" />

### Gestión de Ingresos
<img width="1900" height="876" alt="findata_ingresos" src="https://github.com/user-attachments/assets/5f1f5b65-35c4-4d5b-a4fb-640c9bc45311" />


### Gestión de Gastos
<img width="1901" height="867" alt="findata_gastos" src="https://github.com/user-attachments/assets/852f845c-156b-4b00-ab9f-01d9cc9d1bd2" />


### Historial de Transacciones
<img width="1886" height="865" alt="findata_tabla" src="https://github.com/user-attachments/assets/8173cdf4-73c8-4155-a402-3153d16e1e37" />


---

## 🙏 Agradecimientos

- [SB Admin 2](https://startbootstrap.com/theme/sb-admin-2) por la plantilla de administración
- [Chart.js](https://www.chartjs.org/) - Biblioteca de gráficos
- [DataTables](https://datatables.net/) - Plugin de tablas interactivas
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Render](https://render.com/) por el hosting gratuito

---

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un [issue](https://github.com/tu-usuario/findata/issues) en GitHub.

---

<div align="center">
  <p>© 2025 FinData - Todos los derechos reservados</p>
</div>
