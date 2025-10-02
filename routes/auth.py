from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import MySQLdb.cursors
from werkzeug.security import check_password_hash, generate_password_hash
from utils.auth_helpers import login_required
from utils.password_recovery import recovery_manager
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
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        direccion = request.form["direccion"]
        rol = request.form.get("rol", "cliente")  # Default role is 'cliente'

        hashed_password = generate_password_hash(password)

        try:
            cursor = current_app.db.cursor()

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

            flash("Usuario registrado exitosamente 🚀", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            import traceback
            print("❌ Error al registrar:", str(e))
            flash("Error al registrar: " + str(e), "danger")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
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
            
            # Guardar datos en sesión
            session["usuario_id"] = user["idusu"]
            session["rol"] = user["rolusu"]
            session["logged_in"] = True
            session["user_name"] = user["nomusu"]
            session["role"] = user["rolusu"]
            session["login_time"] = datetime.now().isoformat()  # Para timeout de sesión
    
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
@login_required
def role_dashboard():
    rol = session.get("rol")
    if not rol:
        flash("Rol no reconocido", "danger")
        return redirect(url_for("auth.login"))

    return render_template("role_dashboard.html", rol=rol)


@auth_bp.route("/logout")
def logout():
    # Limpiar todas las variables de sesión
    session.clear()
    flash("Sesión cerrada correctamente 👋", "info")
    return redirect(url_for("index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Página para solicitar recuperación de contraseña"""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash("⚠️ Por favor ingresa un email válido", "warning")
            return render_template("auth/forgot_password.html")
        
        # Crear token de recuperación
        result = recovery_manager.create_recovery_token(email)
        
        if result['success']:
            # En un entorno real, aquí enviarías el email
            # Por ahora mostramos el token en el flash (solo para desarrollo)
            recovery_url = url_for('auth.reset_password', token=result['token'], _external=True)
            
            flash(f"✅ Se ha enviado un enlace de recuperación a tu email. " +
                  f"El enlace expira en 1 hora.<br><br>" +
                  f"<strong>🔗 Enlace de recuperación (DESARROLLO):</strong><br>" +
                  f"<a href='{recovery_url}' class='text-blue-600 underline'>" +
                  f"Recuperar contraseña</a>", "success")
        else:
            flash(f"⚠️ {result['message']}", "warning")
        
        return render_template("auth/forgot_password.html")
    
    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Página para resetear contraseña con token"""
    
    # Validar token
    validation = recovery_manager.validate_recovery_token(token)
    
    if not validation['valid']:
        flash(f"❌ {validation['message']}", "error")
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validaciones
        if not new_password or len(new_password) < 6:
            flash("⚠️ La contraseña debe tener al menos 6 caracteres", "warning")
            return render_template("auth/reset_password.html", 
                                 token=token, 
                                 email=validation['email'],
                                 time_remaining=validation['time_remaining'])
        
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
