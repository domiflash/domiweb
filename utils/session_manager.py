"""
🕐 Sistema de Gestión de Timeout de Sesión
Proporciona middleware y utilidades para gestionar automáticamente:
- Timeout de sesiones por inactividad
- Renovación automática de sesiones
- Alertas de sesión próxima a expirar
- Logout automático por seguridad
"""

from datetime import datetime, timedelta
from functools import wraps
from flask import session, request, jsonify, redirect, url_for, flash, current_app
import time


class SessionTimeoutError(Exception):
    """Excepción personalizada para timeout de sesión"""
    pass


class SessionManager:
    """Gestor centralizado de sesiones con timeout automático"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar el gestor de sesiones con la aplicación Flask"""
        app.session_manager = self
        
        # Configuraciones por defecto
        app.config.setdefault('SESSION_TIMEOUT_MINUTES', 30)
        app.config.setdefault('SESSION_WARNING_MINUTES', 5)
        
        # Registrar middleware
        app.before_request(self.check_session_timeout)
    
    def start_session(self, user_id, role, remember_me=False):
        """
        Iniciar una nueva sesión con timeout
        
        Args:
            user_id: ID del usuario
            role: Rol del usuario
            remember_me: Si la sesión debe ser recordada
        """
        now = datetime.now()
        timeout_minutes = current_app.config.get('SESSION_TIMEOUT_MINUTES', 30)
        
        # Configurar datos de sesión
        session.permanent = remember_me
        session['user_id'] = user_id
        session['role'] = role
        session['login_time'] = now.isoformat()
        session['last_activity'] = now.isoformat()
        session['timeout_minutes'] = timeout_minutes
        session['session_token'] = self._generate_session_token(user_id)
        
        # Configurar tiempo de expiración
        if remember_me:
            session.permanent_session_lifetime = timedelta(days=30)
        else:
            session.permanent_session_lifetime = timedelta(minutes=timeout_minutes)
    
    def refresh_session(self):
        """Renovar la actividad de la sesión actual"""
        if 'user_id' in session:
            session['last_activity'] = datetime.now().isoformat()
            session.modified = True
    
    def get_session_info(self):
        """Obtener información completa de la sesión actual"""
        if 'user_id' not in session:
            return None
        
        last_activity = datetime.fromisoformat(session['last_activity'])
        login_time = datetime.fromisoformat(session['login_time'])
        timeout_minutes = session.get('timeout_minutes', 30)
        warning_minutes = current_app.config.get('SESSION_WARNING_MINUTES', 5)
        
        now = datetime.now()
        time_since_activity = (now - last_activity).total_seconds() / 60
        time_until_timeout = timeout_minutes - time_since_activity
        
        return {
            'user_id': session['user_id'],
            'role': session['role'],
            'login_time': login_time,
            'last_activity': last_activity,
            'timeout_minutes': timeout_minutes,
            'time_since_activity': time_since_activity,
            'time_until_timeout': time_until_timeout,
            'is_expired': time_until_timeout <= 0,
            'needs_warning': time_until_timeout <= warning_minutes,
            'session_token': session.get('session_token')
        }
    
    def check_session_timeout(self):
        """Verificar si la sesión ha expirado (middleware)"""
        # Excluir rutas que no requieren autenticación
        excluded_paths = ['/auth/login', '/auth/register', '/auth/logout', 
                         '/auth/forgot-password', '/auth/reset-password',
                         '/static/', '/session/']
        
        if any(request.path.startswith(path) for path in excluded_paths):
            return
        
        # Verificar si hay sesión activa
        if 'user_id' not in session:
            return
        
        info = self.get_session_info()
        if not info:
            return
        
        # Si la sesión ha expirado
        if info['is_expired']:
            self.end_session('timeout')
            flash('Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Si es una solicitud AJAX, devolver información de sesión
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if info['needs_warning']:
                return jsonify({
                    'session_warning': True,
                    'time_remaining': info['time_until_timeout'],
                    'message': f'Tu sesión expirará en {int(info["time_until_timeout"])} minutos'
                })
    
    def end_session(self, reason='manual'):
        """
        Terminar la sesión actual
        
        Args:
            reason: Razón del logout ('manual', 'timeout', 'security')
        """
        if 'user_id' in session:
            user_id = session['user_id']
            # Limpiar toda la información de sesión
            session.clear()
            
            # Log del evento (opcional)
            print(f"🔚 Sesión terminada - Usuario: {user_id}, Razón: {reason}")
    
    def _generate_session_token(self, user_id):
        """Generar token único para la sesión"""
        import hashlib
        import secrets
        
        data = f"{user_id}_{datetime.now().isoformat()}_{secrets.token_hex(16)}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]


# Instancia global del gestor
session_manager = SessionManager()


def require_active_session(f):
    """
    Decorador para requerir sesión activa y renovarla automáticamente
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'error')
            return redirect(url_for('auth.login'))
        
        # Renovar actividad de sesión
        session_manager.refresh_session()
        
        # Verificar si la sesión necesita advertencia
        info = session_manager.get_session_info()
        if info and info['needs_warning']:
            flash(f'⚠️ Tu sesión expirará en {int(info["time_until_timeout"])} minutos', 'warning')
        
        return f(*args, **kwargs)
    
    return decorated_function


def auto_refresh_session(f):
    """
    Decorador para renovar automáticamente la sesión en acciones importantes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            session_manager.refresh_session()
        return f(*args, **kwargs)
    
    return decorated_function


def get_session_data():
    """Obtener datos de sesión para templates"""
    return session_manager.get_session_info()