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
    
    # ⏰ Configuración de Timeout de Sesión
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))  # 30 minutos por defecto
    SESSION_WARNING_MINUTES = int(os.getenv("SESSION_WARNING_MINUTES", "5"))   # Advertencia 5 min antes
    SESSION_PERMANENT = False  # Las sesiones no son permanentes por defecto
    SESSION_TYPE = 'filesystem'  # Tipo de almacenamiento de sesión
    SESSION_FILE_DIR = os.getenv("SESSION_FILE_DIR", "./flask_session")  # Directorio de sesiones
    
    # 🔒 Configuración de Seguridad de Sesión
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"  # HTTPS en producción
    SESSION_COOKIE_HTTPONLY = True  # Prevenir acceso desde JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF
    
    # 🚫 Límites de Intentos de Login
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))  # Máximo 5 intentos
    LOGIN_ATTEMPT_TIMEOUT_MINUTES = int(os.getenv("LOGIN_ATTEMPT_TIMEOUT_MINUTES", "15"))  # Bloqueo 15 min

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
