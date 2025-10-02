"""
PLAN DE PRUEBAS AUTOMATIZADO - DOMIFLASH
=========================================

USUARIOS DE PRUEBA DISPONIBLES:
- Admin: admin@domiflash (contraseña: 123456)
- Cliente: maicol@domiflash (contraseña: 123456)
- Restaurante: restaurante@domiflash (contraseña: 123456)
- Repartidor: repartidor@test.com (contraseña: 123456)

FASES DE PRUEBA:
1. ✅ Autenticación (Login/Registro)
2. ✅ Módulo Administrador
3. ✅ Módulo Cliente (Menú, Carrito, Checkout)
4. ✅ Módulo Restaurante (Productos, Pedidos)
5. ✅ Módulo Repartidor (Dashboard, Pedidos)

CASOS DE PRUEBA POR MÓDULO:
===============================
ADMIN:
- Gestión usuarios
- Gestión categorías
- Estadísticas generales

CLIENTE:
- Ver menú por restaurantes
- Agregar productos al carrito
- Proceso completo de checkout
- Simulación de pago
- Visualización de pedidos

RESTAURANTE:
- CRUD productos
- Gestión de pedidos
- Cambio de estados

REPARTIDOR:
- Dashboard con estadísticas
- Tomar pedidos disponibles
- Cambiar estados de entrega
"""

# Script de pruebas automatizado
import MySQLdb
from config import Config
import requests
import time

def test_database_connection():
    """Verificar conexión a BD"""
    try:
        db = MySQLdb.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            passwd=Config.DB_PASSWORD,
            db=Config.DB_NAME
        )
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_users = cursor.fetchone()[0]
        cursor.close()
        db.close()
        print(f"[OK] BD Conectada - {total_users} usuarios registrados")
        return True
    except Exception as e:
        print(f"[ERROR] BD: {e}")
        return False

def test_web_server():
    """Verificar servidor web"""
    try:
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        if response.status_code == 200:
            print("[OK] Servidor web funcionando")
            return True
        else:
            print(f"[ERROR] Servidor respondió: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Servidor no responde: {e}")
        return False

if __name__ == "__main__":
    print("INICIANDO PRUEBAS DEL SISTEMA DOMIFLASH")
    print("=" * 50)
    
    # Pruebas básicas
    db_ok = test_database_connection()
    web_ok = test_web_server()
    
    if db_ok and web_ok:
        print("\n✅ SISTEMA LISTO PARA PRUEBAS COMPLETAS")
    else:
        print("\n❌ SISTEMA NO ESTÁ LISTO - REVISAR ERRORES")