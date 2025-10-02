from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import MySQLdb.cursors
from werkzeug.security import check_password_hash, generate_password_hash
from utils.auth_helpers import login_required
from utils.password_recovery import recovery_manager
from utils.validation_decorators import validate_form, require_fields
from utils.input_validator import input_validator
from utils.session_manager import session_manager, require_active_session
from datetime import datetime
import re

auth_bp = Blueprint("auth", __name__)


def obtener_ip_cliente():
    """Obtener la IP real del cliente considerando proxies"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


def obtener_user_agent():
    """Obtener el User-Agent del navegador"""
    return request.headers.get('User-Agent', 'Unknown')


def verificar_cuenta_bloqueada(email):
    """Verificar si una cuenta está bloqueada"""
    try:
        cursor = current_app.db.cursor()
        cursor.callproc("verificar_bloqueo_cuenta", (email, 0, 0, 0))
        
        # Obtener resultados del procedimiento
        cursor.execute("SELECT @_verificar_bloqueo_cuenta_1 as bloqueada, @_verificar_bloqueo_cuenta_2 as intentos, @_verificar_bloqueo_cuenta_3 as tiempo_restante")
        resultado = cursor.fetchone()
        cursor.close()
        
        return {
            'bloqueada': bool(resultado['bloqueada']),
            'intentos': resultado['intentos'],
            'tiempo_restante': resultado['tiempo_restante']
        }
    except Exception as e:
        print(f"❌ Error verificando bloqueo: {e}")
        return {'bloqueada': False, 'intentos': 0, 'tiempo_restante': 0}


def registrar_intento_fallido(email, ip, user_agent):
    """Registrar un intento de login fallido"""
    try:
        cursor = current_app.db.cursor()
        cursor.callproc("incrementar_intentos_fallidos", (email, ip, user_agent))
        current_app.db.commit()
        cursor.close()
    except Exception as e:
        print(f"❌ Error registrando intento fallido: {e}")


def registrar_login_exitoso(email, ip, user_agent):
    """Registrar un login exitoso y resetear intentos"""
    try:
        cursor = current_app.db.cursor()
        cursor.callproc("login_exitoso", (email, ip, user_agent))
        current_app.db.commit()
        cursor.close()
    except Exception as e:
        print(f"❌ Error registrando login exitoso: {e}")


@auth_bp.route("/register", methods=["GET", "POST"])
@validate_form({
    'nombre': 'name',
    'email': 'email', 
    'password': 'password',
    'direccion': 'address',
    'rol': 'role'
})
def register():
    if request.method == "POST":
        # Los datos ya están validados por el decorador
        nombre = request.validated_data["nombre"]
        email = request.validated_data["email"]
        password = request.validated_data["password"]
        direccion = request.validated_data["direccion"]
        rol = request.validated_data.get("rol", "cliente")

        # Verificar si el email ya existe
        cursor = current_app.db.cursor()
        cursor.execute("SELECT idusu FROM usuarios WHERE corusu = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("❌ Este email ya está registrado", "error")
            cursor.close()
            return render_template("auth/register.html")

        try:
            hashed_password = generate_password_hash(password)

            # 👉 Registrar usuario con SP
            cursor.callproc("registrar_usuario", (nombre, email, hashed_password, direccion, rol))
            current_app.db.commit()

            # ✅ Obtener el id del usuario recién creado
            cursor.execute("SELECT LAST_INSERT_ID() AS idusu;")
            nuevo_usuario = cursor.fetchone()
            idusu = nuevo_usuario["idusu"]

            # 👉 Si es restaurante, creamos su registro en la tabla restaurantes
            if rol == "restaurante":
                cursor.execute(
                    "INSERT INTO restaurantes (idusu, nomres, desres, dirres, telres) VALUES (%s, %s, %s, %s, %s)",
                    (idusu, nombre, "Mi restaurante", direccion, "0000000000")
                )
                current_app.db.commit()

            cursor.close()

            flash("✅ Usuario registrado exitosamente 🚀", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            import traceback
            print("❌ Error al registrar:", str(e))
            flash(f"❌ Error al registrar: {str(e)}", "danger")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@validate_form({
    'email': 'email',
    'password': 'password'
})
def login():
    if request.method == "POST":
        # Los datos ya están validados por el decorador
        email = request.validated_data["email"]
        password = request.validated_data["password"]
        ip_cliente = obtener_ip_cliente()
        user_agent = obtener_user_agent()

        # 1. Verificar si la cuenta está bloqueada
        estado_bloqueo = verificar_cuenta_bloqueada(email)
        
        if estado_bloqueo['bloqueada']:
            flash(f"🚫 Cuenta bloqueada por múltiples intentos fallidos. "
                  f"Tiempo restante: {estado_bloqueo['tiempo_restante']} minutos", "danger")
            return render_template("auth/login.html", 
                                   cuenta_bloqueada=True, 
                                   tiempo_restante=estado_bloqueo['tiempo_restante'])

        # 2. Verificar credenciales
        cursor = current_app.db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE corusu=%s AND estusu='activo'", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user["conusu"], password):
            # ✅ LOGIN EXITOSO
            # Registrar login exitoso y resetear intentos
            registrar_login_exitoso(email, ip_cliente, user_agent)
            
            # 🕐 Iniciar sesión con timeout usando el nuevo sistema
            remember_me = request.form.get('remember_me', False)
            session_manager.start_session(user["idusu"], user["rolusu"], remember_me)
            
            # Guardar datos adicionales en sesión (compatibilidad)
            session["logged_in"] = True
            session["user_name"] = user["nomusu"]
    
            flash(f"Bienvenido, {user['nomusu']} 👋", "success")
            return redirect(url_for("auth.role_dashboard"))
        else:
            # ❌ LOGIN FALLIDO
            # Registrar intento fallido
            registrar_intento_fallido(email, ip_cliente, user_agent)
            
            # Verificar nuevo estado después del intento fallido
            nuevo_estado = verificar_cuenta_bloqueada(email)
            
            if nuevo_estado['bloqueada']:
                flash(f"🚫 Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos.", "danger")
                return render_template("auth/login.html", 
                                       cuenta_bloqueada=True, 
                                       tiempo_restante=15)
            else:
                intentos_restantes = 5 - nuevo_estado['intentos']
                if intentos_restantes <= 2:
                    flash(f"⚠️ Credenciales incorrectas. Te quedan {intentos_restantes} intentos.", "warning")
                else:
                    flash("❌ Correo o contraseña incorrectos", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/role_dashboard")
@require_active_session
def role_dashboard():
    rol = session.get("role", session.get("rol"))  # Compatibilidad con ambos nombres
    if not rol:
        flash("Rol no reconocido", "danger")
        return redirect(url_for("auth.login"))

    return render_template("role_dashboard.html", rol=rol)


@auth_bp.route("/logout")
def logout():
    # 🕐 Terminar sesión usando el nuevo sistema
    session_manager.end_session('manual')
    flash("Sesión cerrada correctamente 👋", "info")
    return redirect(url_for("index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@validate_form({
    'email': 'email'
})
def forgot_password():
    """Página para solicitar recuperación de contraseña"""
    if request.method == "POST":
        # Los datos ya están validados por el decorador
        email = request.validated_data["email"]
        
        # Crear token de recuperación y enviar email
        result = recovery_manager.create_recovery_token(email)
        
        if result['success'] and result['email_sent']:
            flash(f"✅ {result['message']}", "success")
        elif result['success'] and not result['email_sent']:
            # Token creado pero email falló - mostrar enlace para desarrollo
            recovery_url = url_for('auth.reset_password', token=result['token'], _external=True)
            flash(f"⚠️ Token creado pero error enviando email. " +
                  f"<br><strong>🔗 Enlace de desarrollo:</strong><br>" +
                  f"<a href='{recovery_url}' class='text-blue-600 underline'>" +
                  f"Recuperar contraseña</a>", "warning")
        else:
            flash(f"❌ {result['message']}", "error")
        
        return render_template("auth/forgot_password.html")
    
    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
@validate_form({
    'password': 'password'
})
def reset_password(token):
    """Página para resetear contraseña con token"""
    
    # Validar token
    validation = recovery_manager.validate_recovery_token(token)
    
    if not validation['valid']:
        flash(f"❌ {validation['message']}", "error")
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == "POST":
        # Los datos ya están validados por el decorador
        new_password = request.validated_data["password"]
        confirm_password = request.form.get("confirm_password", "")
        
        # Validar confirmación de contraseña manualmente
        if new_password != confirm_password:
            flash("⚠️ Las contraseñas no coinciden", "warning")
            return render_template("auth/reset_password.html", 
                                 token=token, 
                                 email=validation['email'],
                                 time_remaining=validation['time_remaining'])
        
        # Encriptar nueva contraseña
        password_hash = generate_password_hash(new_password)
        
        # Cambiar contraseña
        result = recovery_manager.change_password_with_token(token, password_hash)
        
        if result['success']:
            flash("✅ Contraseña cambiada exitosamente. Ya puedes iniciar sesión.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash(f"❌ {result['message']}", "error")
            return redirect(url_for('auth.forgot_password'))
    
    return render_template("auth/reset_password.html", 
                         token=token, 
                         email=validation['email'],
                         time_remaining=validation['time_remaining'])
    return redirect(url_for("index"))
