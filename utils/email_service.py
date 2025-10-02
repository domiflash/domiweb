"""
Servicio de envío de emails para DomiFlash
Maneja todos los emails del sistema: recuperación, notificaciones, etc.
"""

from flask import current_app, render_template_string
from flask_mail import Message
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class EmailService:
    """Servicio centralizado para el envío de emails"""
    
    @staticmethod
    def _get_sender_email():
        """Obtiene el email remitente, con fallback a variables de entorno"""
        try:
            return current_app.config.get('MAIL_DEFAULT_SENDER') or os.getenv('MAIL_DEFAULT_SENDER', 'brayanji890@gmail.com')
        except (RuntimeError, KeyError):
            # Fallback si no hay contexto de Flask
            return os.getenv('MAIL_DEFAULT_SENDER', 'brayanji890@gmail.com')
    
    @staticmethod
    def send_password_recovery_email(email, token, user_name="Usuario"):
        """
        Envía email de recuperación de contraseña
        
        Args:
            email (str): Email del destinatario
            token (str): Token de recuperación
            user_name (str): Nombre del usuario
            
        Returns:
            dict: Resultado del envío
        """
        try:
            # Crear enlace de recuperación
            recovery_url = f"http://127.0.0.1:5000/auth/reset-password/{token}"
            
            # Obtener email remitente
            sender_email = EmailService._get_sender_email()
            
            # Crear mensaje
            msg = Message(
                subject="🔐 Recuperación de Contraseña - DomiFlash",
                recipients=[email],
                sender=sender_email
            )
            
            # Template HTML del email
            html_template = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Recuperación de Contraseña - DomiFlash</title>
                <style>
                    body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }
                    .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                    .header { background: linear-gradient(135deg, #ff6b35, #f7931e); padding: 30px; text-align: center; color: white; }
                    .header h1 { margin: 0; font-size: 28px; font-weight: 600; }
                    .header p { margin: 10px 0 0; opacity: 0.9; }
                    .content { padding: 30px; }
                    .greeting { font-size: 18px; margin-bottom: 20px; color: #2c3e50; }
                    .message { margin-bottom: 25px; line-height: 1.8; }
                    .button-container { text-align: center; margin: 30px 0; }
                    .recovery-button { display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #ff6b35, #f7931e); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; transition: transform 0.2s; }
                    .recovery-button:hover { transform: translateY(-2px); }
                    .info-box { background: #e8f4fd; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 4px; }
                    .warning-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }
                    .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }
                    .footer a { color: #ff6b35; text-decoration: none; }
                    .security-tips { margin-top: 25px; }
                    .security-tips h3 { color: #2c3e50; margin-bottom: 15px; }
                    .security-tips ul { margin: 0; padding-left: 20px; }
                    .security-tips li { margin-bottom: 8px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Header -->
                    <div class="header">
                        <h1>🍕 DomiFlash</h1>
                        <p>Recuperación de Contraseña</p>
                    </div>
                    
                    <!-- Content -->
                    <div class="content">
                        <div class="greeting">
                            ¡Hola {{ user_name }}! 👋
                        </div>
                        
                        <div class="message">
                            Recibimos una solicitud para restablecer tu contraseña en <strong>DomiFlash</strong>. 
                            Si fuiste tú quien hizo esta solicitud, haz clic en el botón de abajo para crear una nueva contraseña.
                        </div>
                        
                        <div class="button-container">
                            <a href="{{ recovery_url }}" class="recovery-button">
                                🔐 Restablecer Contraseña
                            </a>
                        </div>
                        
                        <div class="info-box">
                            <strong>📋 Información importante:</strong><br>
                            • Este enlace es válido por <strong>1 hora</strong><br>
                            • Solo puede usarse una vez<br>
                            • Tu cuenta será desbloqueada automáticamente al cambiar la contraseña
                        </div>
                        
                        <div class="warning-box">
                            <strong>⚠️ ¿No solicitaste este cambio?</strong><br>
                            Si no solicitaste recuperar tu contraseña, ignora este email. 
                            Tu cuenta permanece segura y no se realizarán cambios.
                        </div>
                        
                        <div class="security-tips">
                            <h3>🛡️ Consejos de Seguridad</h3>
                            <ul>
                                <li>Usa una contraseña única de al menos 8 caracteres</li>
                                <li>Combina letras, números y símbolos</li>
                                <li>No compartas tu contraseña con nadie</li>
                                <li>Considera usar un gestor de contraseñas</li>
                            </ul>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer">
                        <p>
                            © 2025 DomiFlash - Plataforma de Delivery<br>
                            <a href="mailto:soporte@domiflash.com">Contactar Soporte</a> | 
                            <a href="#">Términos de Servicio</a> | 
                            <a href="#">Política de Privacidad</a>
                        </p>
                        <p style="margin-top: 15px; font-size: 12px; color: #999;">
                            Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
                            <span style="word-break: break-all;">{{ recovery_url }}</span>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Renderizar template con variables
            msg.html = render_template_string(
                html_template, 
                user_name=user_name, 
                recovery_url=recovery_url,
                email=email
            )
            
            # Versión texto plano
            msg.body = f"""
            Hola {user_name},

            Recibimos una solicitud para restablecer tu contraseña en DomiFlash.

            Para crear una nueva contraseña, visita el siguiente enlace:
            {recovery_url}

            Este enlace es válido por 1 hora y solo puede usarse una vez.

            Si no solicitaste este cambio, puedes ignorar este email.

            Saludos,
            Equipo DomiFlash
            """
            
            # Enviar email
            current_app.mail.send(msg)
            
            return {
                'success': True,
                'message': f'Email de recuperación enviado exitosamente a {email}',
                'email_sent': True
            }
            
        except Exception as e:
            logging.error(f"Error enviando email a {email}: {str(e)}")
            return {
                'success': False,
                'message': f'Error enviando email: {str(e)}',
                'email_sent': False
            }
    
    @staticmethod
    def send_welcome_email(email, user_name):
        """Envía email de bienvenida a nuevos usuarios"""
        try:
            msg = Message(
                subject="🎉 ¡Bienvenido a DomiFlash!",
                recipients=[email],
                sender=EmailService._get_sender_email()
            )
            
            msg.body = f"""
            ¡Hola {user_name}!

            ¡Bienvenido a DomiFlash! Tu cuenta ha sido creada exitosamente.

            Ya puedes comenzar a explorar nuestros restaurantes y realizar pedidos.

            ¡Que disfrutes la experiencia!

            Equipo DomiFlash
            """
            
            current_app.mail.send(msg)
            return True
            
        except Exception as e:
            logging.error(f"Error enviando email de bienvenida: {str(e)}")
            return False
    
    @staticmethod
    def send_order_confirmation_email(email, user_name, order_id, total):
        """Envía email de confirmación de pedido"""
        try:
            msg = Message(
                subject=f"📦 Confirmación de Pedido #{order_id} - DomiFlash",
                recipients=[email],
                sender=EmailService._get_sender_email()
            )
            
            msg.body = f"""
            Hola {user_name},

            Tu pedido #{order_id} ha sido confirmado exitosamente.

            Total: ${total:,.2f}

            Te notificaremos cuando esté listo para entrega.

            ¡Gracias por elegir DomiFlash!

            Equipo DomiFlash
            """
            
            current_app.mail.send(msg)
            return True
            
        except Exception as e:
            logging.error(f"Error enviando confirmación de pedido: {str(e)}")
            return False

# Instancia global del servicio
email_service = EmailService()