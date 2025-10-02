from flask import Flask, render_template
from config import Config
from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.restaurante import restaurante_bp
from routes.repartidor import repartidor_bp
from routes.admin import admin_bp
import pymysql.cursors  # ✅ usamos pymysql
from flask_session import Session
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

    # Conexión a MariaDB con pymysql
    app.db = pymysql.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )

    # Configurar Flask-Session para sesiones persistentes
    app.config['SESSION_TYPE'] = 'filesystem'  # Cambiar a 'redis' si se usa Redis
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cliente_bp, url_prefix="/cliente")
    app.register_blueprint(restaurante_bp, url_prefix="/restaurante")
    app.register_blueprint(repartidor_bp, url_prefix="/repartidor")
    app.register_blueprint(admin_bp, url_prefix="/admin")

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

