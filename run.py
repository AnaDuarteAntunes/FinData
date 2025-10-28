from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # 🔧 CAMBIO: En local usa debug=True, en Render usa debug=False
    # Render no ejecuta este bloque, usa gunicorn directamente
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
