from flask import Flask, render_template
from config import Config
from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.restaurante import restaurante_bp
from routes.repartidor import repartidor_bp
from routes.admin import admin_bp
import MySQLdb
import MySQLdb.cursors
from flask_session import Session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configurations from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DB_HOST'] = os.getenv('DB_HOST')
    app.config['DB_USER'] = os.getenv('DB_USER')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['DB_NAME'] = os.getenv('DB_NAME')

    # Conexión a MySQL
    app.db = MySQLdb.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        passwd=app.config["DB_PASSWORD"],
        db=app.config["DB_NAME"],
        cursorclass=MySQLdb.cursors.DictCursor
    )

    # Configurar Flask-Session para sesiones persistentes
    app.config['SESSION_TYPE'] = 'filesystem'  # Cambiar a 'redis' si se usa Redis
    app.config['SESSION_PERMANENT'] = False  # Las sesiones no serán permanentes
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

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Puerto dinámico
    puerto = int(os.sys.argv[1]) if len(os.sys.argv) > 1 else 5000

    # Abrir navegador automáticamente
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{puerto}")

    modo = os.environ.get("FLASK_ENV", "development")
    if modo == "development":
        print(f"🚀 Modo desarrollo: Flask corriendo en http://127.0.0.1:{puerto}")
        from flask import cli
        cli.show_server_banner = lambda *x: None
        # Ejecuta Flask
        from werkzeug.serving import run_simple
        run_simple("127.0.0.1", puerto, app, use_reloader=True, use_debugger=True)
    else:
        from waitress import serve
        print(f"🚀 Modo producción: Waitress corriendo en http://127.0.0.1:{puerto}")
        serve(app, host="127.0.0.1", port=puerto)
