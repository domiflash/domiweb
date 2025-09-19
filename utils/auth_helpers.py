from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rol = session.get("rol")
            if rol not in allowed_roles:
                flash("No tienes permiso para acceder a esta página", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
