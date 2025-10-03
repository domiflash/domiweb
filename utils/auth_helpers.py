from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Compatibilidad con ambos sistemas de sesión
        user_id = session.get("user_id") or session.get("usuario_id")
        if not user_id:
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Compatibilidad con ambos sistemas de sesión
            rol = session.get("role") or session.get("rol")
            
            if not rol:
                flash("Tu sesión no tiene información de rol. Por favor, inicia sesión nuevamente.", "warning")
                return redirect(url_for("auth.login"))
            
            if rol not in allowed_roles:
                flash(f"No tienes permiso para acceder a esta página. Rol requerido: {', '.join(allowed_roles)}. Tu rol: {rol}", "danger")
                return redirect(url_for("auth.role_dashboard"))
            
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """Decorador específico para rutas de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar login
        user_id = session.get("user_id") or session.get("usuario_id")
        if not user_id:
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for("auth.login"))
        
        # Verificar rol de administrador
        rol = session.get("role") or session.get("rol")
        if rol != "administrador":
            flash(f"Acceso denegado. Esta página es solo para administradores. Tu rol actual: {rol}", "danger")
            return redirect(url_for("auth.role_dashboard"))
        
        return f(*args, **kwargs)

    return decorated_function
