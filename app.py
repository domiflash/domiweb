from flask import Flask, render_template
from config import Config
from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.restaurante import restaurante_bp
from routes.repartidor import repartidor_bp
from routes.admin import admin_bp
from routes.config import config_bp
from routes.session import session_bp
from utils.session_manager import session_manager
import psycopg2  # ✅ PostgreSQL
import psycopg2.extras
from flask_session import Session
from flask_mail import Mail
from dotenv import load_dotenv
import os
import sys

# Cargar variables de entorno desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Cargar configuraciones desde el .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DB_HOST'] = os.getenv('DB_HOST')
    app.config['DB_USER'] = os.getenv('DB_USER')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['DB_NAME'] = os.getenv('DB_NAME')
    
    # Configurar Flask-Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # 🗄️ Configuración de base de datos PostgreSQL con reconexión automática
    def get_db_connection():
        """Obtener conexión a la base de datos PostgreSQL con reconexión automática"""
        try:
            connection = psycopg2.connect(
                host=app.config["DB_HOST"],
                user=app.config["DB_USER"],
                password=app.config["DB_PASSWORD"],
                database=app.config["DB_NAME"],
                cursor_factory=psycopg2.extras.RealDictCursor,
                connect_timeout=10
            )
            connection.autocommit = True
            return connection
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return None
    
    # Función para obtener conexión segura
    def get_db():
        """Obtener conexión de base de datos con manejo de errores"""
        if not hasattr(app, 'db') or app.db is None or app.db.closed:
            app.db = get_db_connection()
        
        try:
            # Probar la conexión actual
            cursor = app.db.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return app.db
        except:
            # Si falla, crear nueva conexión
            print("🔄 Reconectando a la base de datos...")
            app.db = get_db_connection()
            return app.db
    
    # Establecer conexión inicial
    app.db = get_db_connection()
    app.get_db = get_db

    # ⏰ Configurar Flask-Session con timeout y seguridad
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_FILE_DIR'] = './flask_session'
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos en segundos
    Session(app)
    
    # Configurar Flask-Mail
    mail = Mail(app)
    app.mail = mail
    
    # 🕐 Inicializar gestor de sesiones con timeout
    session_manager.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cliente_bp, url_prefix="/cliente")
    app.register_blueprint(restaurante_bp, url_prefix="/restaurante")
    app.register_blueprint(repartidor_bp, url_prefix="/repartidor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(config_bp, url_prefix="/config")
    app.register_blueprint(session_bp, url_prefix="/session")  # 🆕 Nuevo blueprint de sesiones

    @app.route("/index")
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/offline")
    def offline():
        return render_template("offline.html")

    return app

if __name__ == "__main__":
    app = create_app()

    # Puerto dinámico
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    # Solo abrir navegador en el proceso principal
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("FLASK_ENV") == "production":
        import webbrowser
        webbrowser.open(f"http://127.0.0.1:{puerto}")

    modo = os.environ.get("FLASK_ENV", "development")
    if modo == "development":
        print(f"🚀 Modo desarrollo: Flask corriendo en http://127.0.0.1:{puerto}")
        from flask import cli
        cli.show_server_banner = lambda *x: None
        from werkzeug.serving import run_simple
        run_simple("127.0.0.1", puerto, app, use_reloader=True, use_debugger=True)
    else:
        from waitress import serve
        print(f"🚀 Modo producción: Waitress corriendo en http://127.0.0.1:{puerto}")
        serve(app, host="127.0.0.1", port=puerto)
else:
    # Para importaciones desde otros módulos
    app = create_app()

