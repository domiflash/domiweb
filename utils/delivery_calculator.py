"""
UTILIDADES PARA CÁLCULO DE TIEMPO DE ENTREGA
===========================================

Simula funcionalidades reales de apps como Uber Eats, Rappi, etc.
Incluye cálculo de distancia, tiempo estimado, y gestión de ubicaciones.
"""

import math
import random
from datetime import datetime, timedelta
from flask import current_app

class DeliveryCalculator:
    """Calculadora de delivery que simula funcionalidades reales"""
    
    # Coordenadas base para Bogotá (simulamos que toda la app funciona en esta área)
    BASE_LAT = -4.2981
    BASE_LNG = -74.7846
    
    # Parámetros de cálculo (basados en apps reales)
    VELOCIDAD_PROMEDIO_KMH = 25  # km/h velocidad promedio del repartidor
    TIEMPO_PREPARACION_BASE = 15  # minutos base de preparación
    TIEMPO_EXTRA_POR_PRODUCTO = 2  # minutos extra por cada producto adicional
    
    @staticmethod
    def calcular_distancia_haversine(lat1, lng1, lat2, lng2):
        """
        Calcula distancia real entre dos puntos usando fórmula Haversine
        (Como lo hacen las apps reales)
        """
        # Convertir grados a radianes
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        
        # Diferencias
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        # Fórmula Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radio de la Tierra en km
        r = 6371
        
        # Distancia en km
        return c * r
    
    @staticmethod
    def generar_ubicacion_usuario_simulada():
        """
        Genera una ubicación simulada para el usuario
        (En apps reales esto viene del GPS)
        """
        # Generar ubicación aleatoria en un radio de 10km de Bogotá centro
        lat_offset = (random.random() - 0.5) * 0.18  # ~10km radius
        lng_offset = (random.random() - 0.5) * 0.18
        
        return (
            DeliveryCalculator.BASE_LAT + lat_offset,
            DeliveryCalculator.BASE_LNG + lng_offset
        )
    
    @staticmethod
    def calcular_tiempo_estimado(distancia_km, num_productos=1, tipo_preparacion="normal"):
        """
        Calcula tiempo estimado total de entrega
        (Similar a algoritmos de Uber Eats/Rappi)
        
        Factores considerados:
        - Distancia real
        - Número de productos (más productos = más tiempo prep)
        - Tipo de preparación del restaurante
        - Tráfico simulado
        - Buffer de seguridad
        """
        
        # 1. Tiempo de preparación
        tiempo_prep = DeliveryCalculator.TIEMPO_PREPARACION_BASE
        tiempo_prep += (num_productos - 1) * DeliveryCalculator.TIEMPO_EXTRA_POR_PRODUCTO
        
        # Ajuste por tipo de restaurante
        if tipo_preparacion == "rapido":
            tiempo_prep *= 0.8
        elif tipo_preparacion == "lento":
            tiempo_prep *= 1.4
        
        # 2. Tiempo de viaje
        tiempo_viaje = (distancia_km / DeliveryCalculator.VELOCIDAD_PROMEDIO_KMH) * 60
        
        # 3. Factor de tráfico simulado
        factor_trafico = random.uniform(1.1, 1.4)  # Entre 10% y 40% más tiempo
        tiempo_viaje *= factor_trafico
        
        # 4. Buffer de seguridad (apps reales siempre agregan buffer)
        buffer_minutos = random.randint(3, 8)
        
        # Tiempo total
        tiempo_total = int(tiempo_prep + tiempo_viaje + buffer_minutos)
        
        # Redondear a múltiplos de 5 (como hacen las apps reales)
        tiempo_total = round(tiempo_total / 5) * 5
        
        # Mínimo 20 minutos, máximo 60 minutos
        tiempo_total = max(20, min(60, tiempo_total))
        
        return tiempo_total
    
    @staticmethod
    def obtener_ubicacion_restaurante(idres):
        """Obtiene las coordenadas del restaurante desde la BD"""
        db = current_app.get_db()

        cursor = db.cursor()
        cursor.execute("""
            SELECT lat_restaurante, lng_restaurante, nomres
            FROM restaurantes 
            WHERE idres = %s
        """, (idres,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result['lat_restaurante'], result['lng_restaurante'], result['nomres']
        return None
    
    @staticmethod
    def obtener_ubicacion_usuario(idusu):
        """Obtiene o genera ubicación del usuario"""
        db = current_app.get_db()

        cursor = db.cursor()
        cursor.execute("""
            SELECT lat_usuario, lng_usuario 
            FROM usuarios 
            WHERE idusu = %s
        """, (idusu,))
        
        result = cursor.fetchone()
        
        # Si el usuario no tiene ubicación, generar una y guardarla
        if not result or not result['lat_usuario']:
            lat, lng = DeliveryCalculator.generar_ubicacion_usuario_simulada()
            
            cursor.execute("""
                UPDATE usuarios 
                SET lat_usuario = %s, lng_usuario = %s 
                WHERE idusu = %s
            """, (lat, lng, idusu))
            
            db.commit()
            cursor.close()
            return lat, lng
        
        cursor.close()
        return result['lat_usuario'], result['lng_usuario']
    
    @staticmethod
    def calcular_tiempo_para_pedido(idped):
        """
        Función principal: calcula tiempo estimado para un pedido específico
        """
        db = current_app.get_db()

        cursor = db.cursor()
        
        # Obtener datos del pedido
        cursor.execute("""
            SELECT p.idped, p.idusu, p.idres, COUNT(dp.iddet) as num_productos
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
            WHERE p.idped = %s
            GROUP BY p.idped, p.idusu, p.idres
        """, (idped,))
        
        pedido_info = cursor.fetchone()
        cursor.close()
        
        if not pedido_info:
            return None
        
        # Obtener ubicaciones
        try:
            lat_rest, lng_rest, nom_rest = DeliveryCalculator.obtener_ubicacion_restaurante(pedido_info['idres'])
            lat_user, lng_user = DeliveryCalculator.obtener_ubicacion_usuario(pedido_info['idusu'])
            
            # Calcular distancia
            distancia = DeliveryCalculator.calcular_distancia_haversine(
                lat_rest, lng_rest, lat_user, lng_user
            )
            
            # Calcular tiempo estimado
            tiempo_estimado = DeliveryCalculator.calcular_tiempo_estimado(
                distancia, 
                pedido_info['num_productos']
            )
            
            # Calcular hora estimada de entrega
            hora_estimada = datetime.now() + timedelta(minutes=tiempo_estimado)
            
            # Actualizar en la base de datos
            db = current_app.get_db()

            cursor = db.cursor()
            cursor.execute("""
                UPDATE pedidos 
                SET tiempo_estimado_minutos = %s, hora_estimada_entrega = %s
                WHERE idped = %s
            """, (tiempo_estimado, hora_estimada, idped))
            
            db.commit()
            cursor.close()
            
            return {
                'tiempo_estimado': tiempo_estimado,
                'hora_estimada': hora_estimada,
                'distancia_km': round(distancia, 2),
                'restaurante': nom_rest,
                'num_productos': pedido_info['num_productos']
            }
            
        except Exception as e:
            print(f"Error calculando tiempo para pedido {idped}: {e}")
            return None
    
    @staticmethod
    def formatear_tiempo_estimado(minutos):
        """
        Formatea el tiempo estimado como lo hacen las apps reales
        Ejemplos: "25-30 min", "30-35 min"
        """
        if minutos <= 25:
            return f"{minutos-5}-{minutos} min"
        else:
            return f"{minutos}-{minutos+5} min"
    
    @staticmethod
    def obtener_estado_entrega_con_tiempo(idped):
        """
        Obtiene el estado actual del pedido con información de tiempo
        """
        db = current_app.get_db()

        cursor = db.cursor()
        cursor.execute("""
            SELECT estped, tiempo_estimado_minutos, hora_estimada_entrega, fecha_creacion
            FROM pedidos 
            WHERE idped = %s
        """, (idped,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if not result:
            return None
        
        tiempo_transcurrido = (datetime.now() - result['fecha_creacion']).total_seconds() / 60
        tiempo_restante = max(0, result['tiempo_estimado_minutos'] - tiempo_transcurrido)
        
        return {
            'estado': result['estped'],
            'tiempo_estimado_original': result['tiempo_estimado_minutos'],
            'tiempo_restante': int(tiempo_restante),
            'hora_estimada': result['hora_estimada_entrega'],
            'porcentaje_completado': min(100, int((tiempo_transcurrido / result['tiempo_estimado_minutos']) * 100))
        }