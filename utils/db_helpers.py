"""
🗄️ Utilidades para manejo seguro de base de datos
Proporciona funciones para reconexión automática y manejo de errores
"""

from flask import current_app
import pymysql.cursors
import functools
import time


def safe_db_operation(f):
    """
    Decorador para operaciones de base de datos con reconexión automática
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Obtener conexión segura
                db = current_app.get_db()
                if db is None:
                    raise Exception("No se pudo conectar a la base de datos")
                
                # Ejecutar la función
                return f(db, *args, **kwargs)
                
            except (pymysql.err.OperationalError, pymysql.err.InterfaceError) as e:
                print(f"🔄 Intento {attempt + 1}/{max_retries} - Error de BD: {e}")
                
                if attempt < max_retries - 1:
                    # Forzar reconexión
                    current_app.db = None
                    time.sleep(0.5)  # Esperar medio segundo
                    continue
                else:
                    # Si fallaron todos los intentos
                    print(f"❌ Error de base de datos después de {max_retries} intentos")
                    raise Exception("Error de conexión a la base de datos")
            
            except Exception as e:
                print(f"❌ Error general en operación de BD: {e}")
                raise e
    
    return decorated_function


@safe_db_operation
def execute_query(db, query, params=None):
    """
    Ejecutar una consulta SELECT de forma segura
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()


@safe_db_operation
def execute_query_one(db, query, params=None):
    """
    Ejecutar una consulta SELECT que devuelve un solo resultado
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()


@safe_db_operation
def execute_insert(db, query, params=None):
    """
    Ejecutar una consulta INSERT de forma segura
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, params or ())
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()


@safe_db_operation
def execute_update(db, query, params=None):
    """
    Ejecutar una consulta UPDATE de forma segura
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, params or ())
        db.commit()
        return cursor.rowcount
    finally:
        cursor.close()


@safe_db_operation
def execute_procedure(db, procedure_name, params=None):
    """
    Ejecutar un procedimiento almacenado de forma segura
    """
    cursor = db.cursor()
    try:
        cursor.callproc(procedure_name, params or ())
        db.commit()
        
        # Intentar obtener resultados si los hay
        try:
            result = cursor.fetchall()
            return result
        except:
            return None
    finally:
        cursor.close()


def test_db_connection():
    """
    Probar la conexión a la base de datos
    """
    try:
        db = current_app.get_db()
        if db:
            cursor = db.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            return True, "Conexión exitosa"
        else:
            return False, "No se pudo obtener conexión"
    except Exception as e:
        return False, f"Error: {e}"