from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import MySQLdb.cursors
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        direccion = request.form["direccion"]
        rol = request.form["rol"]

        hashed_password = generate_password_hash(password)

        try:
            cursor = current_app.db.cursor()
            cursor.callproc("registrar_usuario", (nombre, email, hashed_password, direccion, rol))
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
        cursor.execute("SELECT * FROM usuarios WHERE corusu=%s AND estusu=1", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user["conusu"], password):
            # Guardar datos en sesión
            session["usuario_id"] = user["idusu"]
            session["rol"] = user["rolusu"]
    
            flash(f"Bienvenido, {user['nomusu']} 👋", "success")

            # Redirigir según rol
            if user["rolusu"] == "cliente":
                return redirect(url_for("cliente.test"))
            elif user["rolusu"] == "restaurante":
                return redirect(url_for("restaurante.test"))
            elif user["rolusu"] == "repartidor":
                return redirect(url_for("repartidor.test"))
            elif user["rolusu"] == "admin":
                return redirect(url_for("admin.test"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))
