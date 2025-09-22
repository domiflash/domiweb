from flask import Flask, session, has_request_context, render_template
from config import Config
from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.restaurante import restaurante_bp
from routes.repartidor import repartidor_bp
from routes.admin import admin_bp
import MySQLdb
import MySQLdb.cursors
import atexit
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

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cliente_bp, url_prefix="/cliente")
    app.register_blueprint(restaurante_bp, url_prefix="/restaurante")
    app.register_blueprint(repartidor_bp, url_prefix="/repartidor")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.teardown_appcontext
    def clear_session_on_shutdown(exception=None):
        if has_request_context():
            session.clear()
            app.logger.info("All sessions cleared on server shutdown.")
        else:
            app.logger.warning("Attempted to clear session outside of request context.")

    @app.route("/index")
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
