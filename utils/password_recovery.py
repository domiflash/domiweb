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
from utils.email_service import email_service
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
        Crea un token de recuperación para el email dado y envía el email
        
        Returns:
            dict: {
                'success': bool,
                'token': str or None,
                'message': str,
                'expires_at': datetime or None,
                'email_sent': bool
            }
        """
        try:
            # Verificar que el usuario existe y está activo
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT nomusu FROM usuarios WHERE corusu = %s AND estusu = 'activo'", (email,))
            user_result = cursor.fetchone()
            
            if not user_result:
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'token': None,
                    'message': 'Usuario no encontrado o inactivo.',
                    'expires_at': None,
                    'email_sent': False
                }
            
            user_name = user_result['nomusu']
            
            # Limpiar tokens expirados antes de verificar
            cursor.execute("DELETE FROM tokens_recuperacion WHERE fecha_expiracion < NOW()")
            
            # Verificar tokens activos para este usuario
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM tokens_recuperacion 
                WHERE email = %s AND usado = FALSE
            """, (email,))
            
            active_tokens = cursor.fetchone()['count']
            
            if active_tokens >= self.max_tokens_per_user:
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'token': None,
                    'message': f'Demasiados tokens activos. Máximo {self.max_tokens_per_user} permitidos.',
                    'expires_at': None,
                    'email_sent': False
                }
            
            # Generar token único
            token = self.generate_secure_token()
            expires_at = datetime.now() + timedelta(hours=self.token_expiry_hours)
            
            # Obtener información de la solicitud
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', 
                                           request.environ.get('REMOTE_ADDR', 'unknown'))
            user_agent = request.headers.get('User-Agent', 'unknown')
            
            # Insertar nuevo token usando la estructura actual
            cursor.execute("""
                INSERT INTO tokens_recuperacion 
                (email, token, fecha_creacion, fecha_expiracion, usado, ip_solicitud, user_agent)
                VALUES (%s, %s, NOW(), %s, FALSE, %s, %s)
            """, (email, token, expires_at, ip_address, user_agent))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Enviar email de recuperación
            email_result = email_service.send_password_recovery_email(
                email=email,
                token=token,
                user_name=user_name
            )
            
            if email_result['success']:
                return {
                    'success': True,
                    'token': token,
                    'message': f'Email de recuperación enviado exitosamente a {email}. Revisa tu bandeja de entrada.',
                    'expires_at': expires_at,
                    'email_sent': True
                }
            else:
                return {
                    'success': True,  # Token fue creado exitosamente
                    'token': token,
                    'message': f'Token creado pero error enviando email: {email_result["message"]}',
                    'expires_at': expires_at,
                    'email_sent': False
                }
                
        except Exception as e:
            print(f"❌ Error en create_recovery_token: {e}")
            return {
                'success': False,
                'token': None,
                'message': f'Error al crear token: {str(e)}',
                'expires_at': None,
                'email_sent': False
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
            cursor = conn.cursor(dictionary=True)
            
            # Limpiar tokens expirados primero
            cursor.execute("DELETE FROM tokens_recuperacion WHERE fecha_expiracion < NOW()")
            
            # Validar token usando la estructura actual
            cursor.execute("""
                SELECT email, fecha_expiracion, usado
                FROM tokens_recuperacion 
                WHERE token = %s
            """, (token,))
            
            token_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not token_data:
                return {
                    'valid': False,
                    'email': None,
                    'time_remaining': 0,
                    'message': 'Token no encontrado'
                }
            
            if token_data['usado']:
                return {
                    'valid': False,
                    'email': None,
                    'time_remaining': 0,
                    'message': 'Token ya fue usado'
                }
            
            # Verificar si está expirado
            expiracion = token_data['fecha_expiracion']
            ahora = datetime.now()
            
            if expiracion < ahora:
                return {
                    'valid': False,
                    'email': None,
                    'time_remaining': 0,
                    'message': 'Token expirado'
                }
            
            # Calcular tiempo restante en minutos
            tiempo_restante = int((expiracion - ahora).total_seconds() / 60)
            
            return {
                'valid': True,
                'email': token_data['email'],
                'time_remaining': tiempo_restante,
                'message': 'Token válido'
            }
                
        except Exception as e:
            print(f"❌ Error en validate_recovery_token: {e}")
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
            
            email = validation['email']
            
            # Conectar y cambiar contraseña
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Actualizar la contraseña del usuario
            cursor.execute("""
                UPDATE usuarios 
                SET conusu = %s 
                WHERE corusu = %s AND estusu = 'activo'
            """, (new_password_hash, email))
            
            # Marcar el token como usado
            cursor.execute("""
                UPDATE tokens_recuperacion 
                SET usado = TRUE 
                WHERE token = %s
            """, (token,))
            
            # Verificar que se cambió la contraseña
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'message': 'Contraseña cambiada exitosamente',
                    'email': email
                }
            else:
                conn.rollback()
                cursor.close()
                conn.close()
                
                return {
                    'success': False,
                    'message': 'Error: Usuario no encontrado o inactivo',
                    'email': None
                }
                
        except Exception as e:
            print(f"❌ Error en change_password_with_token: {e}")
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
            
            # Limpiar directamente tokens expirados usando la estructura actual
            cursor.execute("DELETE FROM tokens_recuperacion WHERE fecha_expiracion < NOW()")
            deleted_count = cursor.rowcount
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Limpieza de tokens: {deleted_count} tokens expirados eliminados")
            return True
            
        except Exception as e:
            print(f"❌ Error al limpiar tokens expirados: {e}")
            return False
    
    def get_recovery_stats(self, days=7):
        """Obtiene estadísticas de recuperación de contraseñas"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Estadísticas básicas usando la estructura actual
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_tokens,
                    COUNT(CASE WHEN usado = TRUE THEN 1 END) as tokens_usados,
                    COUNT(CASE WHEN fecha_expiracion < NOW() THEN 1 END) as tokens_expirados,
                    COUNT(CASE WHEN usado = FALSE AND fecha_expiracion >= NOW() THEN 1 END) as tokens_activos
                FROM tokens_recuperacion 
                WHERE fecha_creacion >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """, (days,))
            
            stats = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return [stats] if stats else []
            
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return []

# Instancia global del gestor
recovery_manager = PasswordRecoveryManager()