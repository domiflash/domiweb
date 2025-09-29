from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import MySQLdb.cursors
from werkzeug.security import check_password_hash, generate_password_hash
from utils.auth_helpers import login_required

auth_bp = Blueprint("auth", __name__)


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

        cursor = current_app.db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE corusu=%s AND estusu='activo'", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user["conusu"], password):
            # Guardar datos en sesión
            session["usuario_id"] = user["idusu"]
            session["rol"] = user["rolusu"]
            session["logged_in"] = True
            session["user_name"] = user["nomusu"]
            session["role"] = user["rolusu"]  # Para compatibilidad con la navbar
    
            flash(f"Bienvenido, {user['nomusu']} 👋", "success")

            # Redirigir a role_dashboard para todos los roles
            return redirect(url_for("auth.role_dashboard"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

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
