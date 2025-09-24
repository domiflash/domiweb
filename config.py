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
