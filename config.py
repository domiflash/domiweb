from dotenv import load_dotenv
import os   # 👈 este import faltaba

# Cargar variables del archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "fallback-inseguro-para-dev"
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")   # vacío si no hay contraseña
    DB_NAME = os.getenv("DB_NAME", "dbflash")
    
    # Configuración Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Tu email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Contraseña de aplicación
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")  # Email remitente

# Configuración para mysql-connector-python
DB_CONFIG = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'autocommit': True
}
