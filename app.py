from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.restaurante import restaurante_bp
from routes.repartidor import repartidor_bp
from routes.admin import admin_bp
import MySQLdb
import MySQLdb.cursors
from flask import session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    @app.route("/")
    def index():
        return "Bienvenido a DomiFlash 🚀"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
