from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from utils.auth_helpers import login_required, role_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/test")
@login_required
def test():
    return "Ruta de Administrador funcionando 🚀"

@admin_bp.route("/users", methods=["GET"])
@role_required("administrador")
def list_users():
    cursor = current_app.db.cursor()
    cursor.execute("SELECT idusu, nomusu, corusu, dirusu, rolusu, estusu FROM usuarios")
    users = cursor.fetchall()
    return render_template("admin/dashboard.html", users=users)

@admin_bp.route("/users/update/<int:user_id>", methods=["POST"])
@role_required("administrador")
def update_user(user_id):
    nomusu = request.form["nomusu"]
    corusu = request.form["corusu"]
    dirusu = request.form["dirusu"]
    rolusu = request.form["rolusu"]

    cursor = current_app.db.cursor()
    cursor.execute(
        "UPDATE usuarios SET nomusu=%s, corusu=%s, dirusu=%s, rolusu=%s WHERE idusu=%s",
        (nomusu, corusu, dirusu, rolusu, user_id),
    )
    current_app.db.commit()
    flash("Usuario actualizado correctamente", "success")
    return redirect(url_for("admin.list_users"))

@admin_bp.route("/users/deactivate/<int:user_id>", methods=["POST"])
@role_required("administrador")
def deactivate_user(user_id):
    cursor = current_app.db.cursor()
    cursor.execute("UPDATE usuarios SET estusu='inactivo' WHERE idusu=%s", (user_id,))
    current_app.db.commit()
    flash("Usuario desactivado correctamente", "info")
    return redirect(url_for("admin.list_users"))

@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@login_required
@role_required('administrador')
def toggle_user_status(user_id):
    cursor = current_app.db.cursor()
    try:
        current_app.logger.info(f"Attempting to toggle status for user_id: {user_id}")
        cursor.execute("SELECT estusu FROM usuarios WHERE idusu = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            current_app.logger.info(f"User found with id {user_id} and status: {user['estusu']}")
            new_status = 'inactivo' if user['estusu'] == 'activo' else 'activo'
            cursor.execute("UPDATE usuarios SET estusu = %s WHERE idusu = %s", (new_status, user_id))
            current_app.db.commit()
            flash(f"El estado del usuario ha sido cambiado a {new_status}.", "success")
        else:
            current_app.logger.error(f"No user found with id {user_id}. Query result: {user}")
            flash("Usuario no encontrado.", "error")
    except Exception as e:
        current_app.db.rollback()
        flash("Ocurrió un error al cambiar el estado del usuario.", "error")
        current_app.logger.error(f"Error in toggle_user_status: {e}")
    finally:
        cursor.close()

    return redirect(url_for('admin.list_users'))
