"""
Utilidades para el sistema de recuperación de contraseña
Maneja generación de tokens, validación y envío de emails
"""

import secrets
import string
from datetime import datetime, timedelta
import mysql.connector
from config import DB_CONFIG
from flask import request
import hashlib
import os

class PasswordRecoveryManager:
    """Gestor del sistema de recuperación de contraseñas"""
    
    def __init__(self):
        self.token_length = 32
        self.token_expiry_hours = 1
        self.max_tokens_per_user = 3
    
    def generate_secure_token(self):
        """Genera un token seguro para recuperación"""
        # Combinar timestamp + random + hash para mayor seguridad
        timestamp = str(int(datetime.now().timestamp()))
        random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                             for _ in range(self.token_length))
        
        # Crear hash único
        combined = f"{timestamp}_{random_part}_{secrets.token_hex(16)}"
        token = hashlib.sha256(combined.encode()).hexdigest()
        
        return token
    
    def create_recovery_token(self, email):
        """
        Crea un token de recuperación para el email dado
        
        Returns:
            dict: {
                'success': bool,
                'token': str or None,
                'message': str,
                'expires_at': datetime or None
            }
        """
        try:
            # Generar token único
            token = self.generate_secure_token()
            
            # Obtener información de la solicitud
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', 
                                           request.environ.get('REMOTE_ADDR', 'unknown'))
            user_agent = request.headers.get('User-Agent', 'unknown')
            
            # Conectar a la base de datos
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Llamar al procedimiento almacenado
            cursor.callproc('crear_token_recuperacion', 
                          [email, token, ip_address, user_agent, None])
            
            # Obtener resultado
            for result in cursor.stored_results():
                output_params = result.fetchall()
            
            # Obtener parámetro de salida
            cursor.execute("SELECT @_crear_token_recuperacion_4")
            token_creado = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if token_creado:
                expires_at = datetime.now() + timedelta(hours=self.token_expiry_hours)
                return {
                    'success': True,
                    'token': token,
                    'message': 'Token de recuperación creado exitosamente',
                    'expires_at': expires_at
                }
            else:
                return {
                    'success': False,
                    'token': None,
                    'message': 'No se pudo crear el token. Usuario no encontrado o demasiados tokens activos.',
                    'expires_at': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'token': None,
                'message': f'Error al crear token: {str(e)}',
                'expires_at': None
            }
    
    def validate_recovery_token(self, token):
        """
        Valida un token de recuperación
        
        Returns:
            dict: {
                'valid': bool,
                'email': str or None,
                'time_remaining': int (minutos),
                'message': str
            }
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Llamar al procedimiento almacenado
            cursor.callproc('validar_token_recuperacion', [token, None, None, None])
            
            # Obtener parámetros de salida
            cursor.execute("SELECT @_validar_token_recuperacion_1, @_validar_token_recuperacion_2, @_validar_token_recuperacion_3")
            result = cursor.fetchone()
            
            valido, email, tiempo_restante = result
            
            cursor.close()
            conn.close()
            
            if valido:
                return {
                    'valid': True,
                    'email': email,
                    'time_remaining': tiempo_restante,
                    'message': 'Token válido'
                }
            else:
                return {
                    'valid': False,
                    'email': None,
                    'time_remaining': 0,
                    'message': 'Token inválido o expirado'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'email': None,
                'time_remaining': 0,
                'message': f'Error al validar token: {str(e)}'
            }
    
    def change_password_with_token(self, token, new_password_hash):
        """
        Cambia la contraseña usando un token de recuperación
        
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'email': str or None
            }
        """
        try:
            # Primero validar el token
            validation = self.validate_recovery_token(token)
            
            if not validation['valid']:
                return {
                    'success': False,
                    'message': validation['message'],
                    'email': None
                }
            
            # Obtener IP para auditoría
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', 
                                           request.environ.get('REMOTE_ADDR', 'unknown'))
            
            # Conectar y cambiar contraseña
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Llamar al procedimiento almacenado
            cursor.callproc('cambiar_password_con_token', 
                          [token, new_password_hash, ip_address, None])
            
            # Obtener resultado
            cursor.execute("SELECT @_cambiar_password_con_token_3")
            cambiado = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if cambiado:
                return {
                    'success': True,
                    'message': 'Contraseña cambiada exitosamente',
                    'email': validation['email']
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al cambiar la contraseña',
                    'email': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al cambiar contraseña: {str(e)}',
                'email': None
            }
    
    def cleanup_expired_tokens(self):
        """Limpia tokens expirados de la base de datos"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.callproc('limpiar_tokens_expirados')
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error al limpiar tokens expirados: {e}")
            return False
    
    def get_recovery_stats(self, days=7):
        """Obtiene estadísticas de recuperación de contraseñas"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.callproc('estadisticas_recuperacion', [days])
            
            stats = []
            for result in cursor.stored_results():
                stats = result.fetchall()
            
            cursor.close()
            conn.close()
            
            return stats
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return []

# Instancia global del gestor
recovery_manager = PasswordRecoveryManager()