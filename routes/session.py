"""
🔗 Blueprint para gestión de sesiones y endpoints de timeout
Proporciona rutas para:
- Verificar estado de sesión
- Renovar sesión activa
- Obtener tiempo restante
- Logout por timeout
"""

from flask import Blueprint, jsonify, session, request, redirect, url_for, flash
from utils.session_manager import session_manager, require_active_session
from datetime import datetime

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('/status')
def session_status():
    """
    Obtener estado actual de la sesión (para AJAX)
    Retorna información de timeout y advertencias
    """
    info = session_manager.get_session_info()
    
    if not info:
        return jsonify({
            'authenticated': False,
            'message': 'No hay sesión activa'
        })
    
    return jsonify({
        'authenticated': True,
        'user_id': info['user_id'],
        'role': info['role'],
        'time_until_timeout': round(info['time_until_timeout'], 1),
        'is_expired': info['is_expired'],
        'needs_warning': info['needs_warning'],
        'login_time': info['login_time'].isoformat(),
        'last_activity': info['last_activity'].isoformat(),
        'session_token': info['session_token']
    })


@session_bp.route('/refresh', methods=['POST'])
@require_active_session
def refresh_session():
    """
    Renovar la sesión activa (para AJAX)
    Extiende el tiempo de timeout
    """
    session_manager.refresh_session()
    info = session_manager.get_session_info()
    
    return jsonify({
        'success': True,
        'message': 'Sesión renovada exitosamente',
        'new_timeout': round(info['time_until_timeout'], 1),
        'last_activity': info['last_activity'].isoformat()
    })


@session_bp.route('/extend', methods=['POST'])
@require_active_session
def extend_session():
    """
    Extender la sesión por el tiempo completo (reset completo)
    """
    # Reiniciar completamente la actividad
    session['last_activity'] = datetime.now().isoformat()
    session.modified = True
    
    info = session_manager.get_session_info()
    
    return jsonify({
        'success': True,
        'message': 'Sesión extendida por tiempo completo',
        'new_timeout': round(info['time_until_timeout'], 1),
        'extended_at': datetime.now().isoformat()
    })


@session_bp.route('/warning')
@require_active_session
def session_warning():
    """
    Endpoint para obtener advertencias de sesión próxima a expirar
    """
    info = session_manager.get_session_info()
    
    if not info['needs_warning']:
        return jsonify({
            'warning': False,
            'message': 'Sesión en buen estado'
        })
    
    return jsonify({
        'warning': True,
        'time_remaining': round(info['time_until_timeout'], 1),
        'message': f'Tu sesión expirará en {int(info["time_until_timeout"])} minutos',
        'can_extend': True
    })


@session_bp.route('/logout-timeout')
def logout_timeout():
    """
    Logout automático por timeout de sesión
    """
    session_manager.end_session('timeout')
    flash('🕐 Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.', 'warning')
    return redirect(url_for('auth.login'))


@session_bp.route('/logout-security')
def logout_security():
    """
    Logout forzado por razones de seguridad
    """
    session_manager.end_session('security')
    flash('🔒 Tu sesión ha sido cerrada por motivos de seguridad. Por favor, inicia sesión nuevamente.', 'error')
    return redirect(url_for('auth.login'))


@session_bp.route('/heartbeat', methods=['POST'])
def session_heartbeat():
    """
    Endpoint para mantener la sesión activa (heartbeat)
    Se puede llamar periódicamente desde JavaScript
    """
    if 'user_id' not in session:
        return jsonify({
            'authenticated': False,
            'action': 'redirect_login'
        })
    
    # Verificar si la sesión sigue válida
    info = session_manager.get_session_info()
    
    if info['is_expired']:
        session_manager.end_session('timeout')
        return jsonify({
            'authenticated': False,
            'expired': True,
            'action': 'redirect_login',
            'message': 'Sesión expirada'
        })
    
    # Renovar sesión si está activa
    session_manager.refresh_session()
    
    return jsonify({
        'authenticated': True,
        'time_remaining': round(info['time_until_timeout'], 1),
        'needs_warning': info['needs_warning'],
        'last_activity': datetime.now().isoformat()
    })


@session_bp.route('/info')
@require_active_session
def session_info():
    """
    Información detallada de la sesión (para debugging/admin)
    """
    info = session_manager.get_session_info()
    
    return jsonify({
        'session_data': {
            'user_id': info['user_id'],
            'role': info['role'],
            'login_time': info['login_time'].isoformat(),
            'last_activity': info['last_activity'].isoformat(),
            'timeout_minutes': info['timeout_minutes'],
            'time_since_activity': round(info['time_since_activity'], 2),
            'time_until_timeout': round(info['time_until_timeout'], 2),
            'is_expired': info['is_expired'],
            'needs_warning': info['needs_warning'],
            'session_token': info['session_token'][:8] + '...'  # Solo mostrar parte del token
        },
        'server_time': datetime.now().isoformat()
    })