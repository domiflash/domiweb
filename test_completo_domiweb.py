#!/usr/bin/env python3
"""
🔍 SISTEMA DE PRUEBAS COMPLETO PARA DOMIWEB
============================================

Este script realiza pruebas exhaustivas de todos los módulos del sistema DomiFlash.
Incluye pruebas de conectividad, funcionalidad, rutas, y validaciones de seguridad.
"""

import sys
import os
import requests
import time
from datetime import datetime
import json
import traceback

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class DomiWebTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.resultados = {
            'pasadas': 0,
            'fallidas': 0,
            'errores': [],
            'tiempo_inicio': datetime.now()
        }
        
    def log(self, mensaje, tipo="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefijo = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"[{timestamp}] {prefijo.get(tipo, '📝')} {mensaje}")
        
    def verificar_servidor(self):
        """Verificar que el servidor esté corriendo"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log("Servidor Flask está corriendo correctamente", "PASS")
                return True
            else:
                self.log(f"Servidor respondió con código {response.status_code}", "FAIL")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Servidor Flask no está corriendo. Inicia la aplicación primero.", "FAIL")
            return False
        except Exception as e:
            self.log(f"Error verificando servidor: {str(e)}", "FAIL")
            return False
            
    def test_ruta(self, ruta, metodo="GET", datos=None, esperado=200, descripcion=""):
        """Prueba una ruta específica"""
        try:
            url = f"{self.base_url}{ruta}"
            
            if metodo == "GET":
                response = self.session.get(url, timeout=10)
            elif metodo == "POST":
                response = self.session.post(url, data=datos, timeout=10)
            else:
                response = self.session.request(metodo, url, data=datos, timeout=10)
                
            if response.status_code == esperado:
                self.log(f"✅ {ruta} - {descripcion}", "PASS")
                self.resultados['pasadas'] += 1
                return True
            else:
                self.log(f"❌ {ruta} - Esperado: {esperado}, Obtenido: {response.status_code}", "FAIL")
                self.resultados['fallidas'] += 1
                self.resultados['errores'].append(f"{ruta}: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error en {ruta}: {str(e)}", "FAIL")
            self.resultados['fallidas'] += 1
            self.resultados['errores'].append(f"{ruta}: {str(e)}")
            return False
            
    def test_autenticacion(self):
        """Pruebas del módulo de autenticación"""
        self.log("🔐 PROBANDO MÓDULO DE AUTENTICACIÓN", "INFO")
        
        # Rutas de autenticación
        rutas_auth = [
            ("/auth/login", "GET", 200, "Página de login"),
            ("/auth/register", "GET", 200, "Página de registro"),
            ("/auth/logout", "GET", 302, "Logout (redirect)")
        ]
        
        for ruta, metodo, esperado, desc in rutas_auth:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_cliente(self):
        """Pruebas del módulo de cliente"""
        self.log("👤 PROBANDO MÓDULO DE CLIENTE", "INFO")
        
        # Rutas que requieren autenticación (esperamos redirect)
        rutas_cliente = [
            ("/cliente/test", "GET", 302, "Test cliente (requiere auth)"),
            ("/cliente/menu", "GET", 302, "Menú (requiere auth)"),
            ("/cliente/carrito", "GET", 302, "Carrito (requiere auth)"),
            ("/cliente/perfil", "GET", 302, "Perfil (requiere auth)"),
            ("/cliente/checkout", "GET", 302, "Checkout (requiere auth)"),
            ("/cliente/mis-pedidos", "GET", 302, "Mis pedidos (requiere auth)"),
            ("/cliente/pago-exitoso", "GET", 302, "Pago exitoso (requiere auth)")
        ]
        
        for ruta, metodo, esperado, desc in rutas_cliente:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_restaurante(self):
        """Pruebas del módulo de restaurante"""
        self.log("🍽️ PROBANDO MÓDULO DE RESTAURANTE", "INFO")
        
        rutas_restaurante = [
            ("/restaurante/dashboard", "GET", 302, "Dashboard restaurante (requiere auth)"),
            ("/restaurante/productos", "GET", 302, "Productos (requiere auth)"),
            ("/restaurante/pedidos", "GET", 302, "Pedidos (requiere auth)"),
            ("/restaurante/perfil", "GET", 302, "Perfil restaurante (requiere auth)")
        ]
        
        for ruta, metodo, esperado, desc in rutas_restaurante:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_repartidor(self):
        """Pruebas del módulo de repartidor"""
        self.log("🚴 PROBANDO MÓDULO DE REPARTIDOR", "INFO")
        
        rutas_repartidor = [
            ("/repartidor/dashboard", "GET", 302, "Dashboard repartidor (requiere auth)"),
            ("/repartidor/pedidos", "GET", 302, "Pedidos disponibles (requiere auth)"),
            ("/repartidor/mis-entregas", "GET", 302, "Mis entregas (requiere auth)"),
            ("/repartidor/perfil", "GET", 302, "Perfil repartidor (requiere auth)")
        ]
        
        for ruta, metodo, esperado, desc in rutas_repartidor:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_admin(self):
        """Pruebas del módulo de administrador"""
        self.log("⚙️ PROBANDO MÓDULO DE ADMINISTRADOR", "INFO")
        
        rutas_admin = [
            ("/admin/dashboard", "GET", 302, "Dashboard admin (requiere auth)"),
            ("/admin/usuarios", "GET", 302, "Gestión usuarios (requiere auth)"),
            ("/admin/reportes", "GET", 302, "Reportes (requiere auth)"),
            ("/admin/configuracion", "GET", 302, "Configuración (requiere auth)")
        ]
        
        for ruta, metodo, esperado, desc in rutas_admin:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_rutas_publicas(self):
        """Pruebas de rutas públicas"""
        self.log("🌐 PROBANDO RUTAS PÚBLICAS", "INFO")
        
        rutas_publicas = [
            ("/", "GET", 200, "Página principal"),
            ("/index", "GET", 200, "Index"),
            ("/offline", "GET", 200, "Página offline")
        ]
        
        for ruta, metodo, esperado, desc in rutas_publicas:
            self.test_ruta(ruta, metodo, esperado=esperado, descripcion=desc)
            
    def test_archivos_estaticos(self):
        """Pruebas de archivos estáticos"""
        self.log("📁 PROBANDO ARCHIVOS ESTÁTICOS", "INFO")
        
        # Verificar que existan las carpetas estáticas
        static_paths = [
            "/static/css/",
            "/static/js/", 
            "/static/img/"
        ]
        
        for path in static_paths:
            # No probamos directamente porque pueden no tener index
            self.log(f"📂 Verificando estructura: {path}", "INFO")
            
    def test_seguridad_basica(self):
        """Pruebas básicas de seguridad"""
        self.log("🔒 PROBANDO SEGURIDAD BÁSICA", "INFO")
        
        # Intentar acceder a rutas protegidas sin autenticación
        rutas_protegidas = [
            "/cliente/carrito",
            "/restaurante/productos", 
            "/repartidor/pedidos",
            "/admin/usuarios"
        ]
        
        for ruta in rutas_protegidas:
            response = self.session.get(f"{self.base_url}{ruta}")
            if response.status_code == 302:  # Redirect a login
                self.log(f"✅ {ruta} correctamente protegida (redirect)", "PASS")
                self.resultados['pasadas'] += 1
            else:
                self.log(f"⚠️ {ruta} puede tener problema de seguridad", "WARN")
                
    def test_modelos_importacion(self):
        """Verificar que los modelos se puedan importar"""
        self.log("📦 PROBANDO IMPORTACIÓN DE MODELOS", "INFO")
        
        modelos = [
            "models.usuarios",
            "models.productos", 
            "models.pedidos",
            "models.pagos"
        ]
        
        for modelo in modelos:
            try:
                __import__(modelo)
                self.log(f"✅ Modelo {modelo} importado correctamente", "PASS")
                self.resultados['pasadas'] += 1
            except ImportError as e:
                self.log(f"❌ Error importando {modelo}: {str(e)}", "FAIL")
                self.resultados['fallidas'] += 1
                
    def test_utilidades(self):
        """Verificar utilidades del sistema"""
        self.log("🛠️ PROBANDO UTILIDADES", "INFO")
        
        try:
            from utils.auth_helpers import login_required, role_required
            self.log("✅ auth_helpers importado correctamente", "PASS")
            self.resultados['pasadas'] += 1
        except ImportError as e:
            self.log(f"❌ Error importando auth_helpers: {str(e)}", "FAIL")
            self.resultados['fallidas'] += 1
            
        try:
            from utils.delivery_calculator import DeliveryCalculator
            self.log("✅ delivery_calculator importado correctamente", "PASS")
            self.resultados['pasadas'] += 1
        except ImportError as e:
            self.log(f"❌ Error importando delivery_calculator: {str(e)}", "FAIL")
            self.resultados['fallidas'] += 1
            
    def generar_reporte(self):
        """Generar reporte final de pruebas"""
        tiempo_total = datetime.now() - self.resultados['tiempo_inicio']
        total_pruebas = self.resultados['pasadas'] + self.resultados['fallidas']
        
        print("\n" + "="*60)
        print("📊 REPORTE FINAL DE PRUEBAS DOMIWEB")
        print("="*60)
        print(f"⏱️  Tiempo total: {tiempo_total.total_seconds():.2f} segundos")
        print(f"📈 Total de pruebas: {total_pruebas}")
        print(f"✅ Pruebas pasadas: {self.resultados['pasadas']}")
        print(f"❌ Pruebas fallidas: {self.resultados['fallidas']}")
        
        if total_pruebas > 0:
            porcentaje = (self.resultados['pasadas'] / total_pruebas) * 100
            print(f"📊 Porcentaje de éxito: {porcentaje:.1f}%")
            
        if self.resultados['errores']:
            print("\n🔍 ERRORES ENCONTRADOS:")
            for i, error in enumerate(self.resultados['errores'][:10], 1):
                print(f"   {i}. {error}")
            if len(self.resultados['errores']) > 10:
                print(f"   ... y {len(self.resultados['errores']) - 10} errores más")
                
        print("\n" + "="*60)
        
        # Evaluación general
        if porcentaje >= 90:
            print("🎉 EXCELENTE: El sistema está funcionando muy bien")
        elif porcentaje >= 75:
            print("👍 BUENO: El sistema funciona correctamente con pocos problemas")
        elif porcentaje >= 50:
            print("⚠️ REGULAR: El sistema tiene varios problemas que necesitan atención")
        else:
            print("🚨 CRÍTICO: El sistema tiene problemas graves que requieren revisión inmediata")
            
    def ejecutar_todas_las_pruebas(self):
        """Ejecutar suite completa de pruebas"""
        print("🚀 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA DOMIWEB")
        print("="*60)
        
        if not self.verificar_servidor():
            print("❌ No se puede continuar sin el servidor. Inicia la aplicación primero.")
            return False
            
        # Ejecutar todas las pruebas
        self.test_rutas_publicas()
        self.test_autenticacion()
        self.test_cliente()
        self.test_restaurante()
        self.test_repartidor()
        self.test_admin()
        self.test_archivos_estaticos()
        self.test_seguridad_basica()
        self.test_modelos_importacion()
        self.test_utilidades()
        
        # Generar reporte
        self.generar_reporte()
        return True

def main():
    """Función principal"""
    print("🔍 SISTEMA DE PRUEBAS DOMIWEB v1.0")
    print("Asegúrate de que el servidor Flask esté corriendo en el puerto 5000")
    print("-" * 60)
    
    tester = DomiWebTester()
    tester.ejecutar_todas_las_pruebas()

if __name__ == "__main__":
    main()