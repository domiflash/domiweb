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
    db = current_app.get_db()

    cursor = db.cursor()
    cursor.execute("SELECT idusu, nomusu, corusu, dirusu, rolusu, estusu FROM usuarios")
    users = cursor.fetchall()
    return render_template("admin/dashboard.html", users=users)

@admin_bp.route("/users/update/<int:user_id>", methods=["POST"])
@role_required("administrador")
def update_user(user_id):
    nomusu = request.form["nomusu"]
    dirusu = request.form["dirusu"]
    rolusu = request.form["rolusu"]

    db = current_app.get_db()


    cursor = db.cursor()
    try:
        # Actualizar el usuario (sin incluir el email)
        cursor.execute(
            "UPDATE usuarios SET nomusu=%s, dirusu=%s, rolusu=%s WHERE idusu=%s",
            (nomusu, dirusu, rolusu, user_id),
        )
        db.commit()
        flash("Usuario actualizado correctamente", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error al actualizar usuario: {str(e)}", "error")
    finally:
        cursor.close()
    
    return redirect(url_for("admin.list_users"))

@admin_bp.route("/users/deactivate/<int:user_id>", methods=["POST"])
@role_required("administrador")
def deactivate_user(user_id):
    db = current_app.get_db()

    cursor = db.cursor()
    cursor.execute("UPDATE usuarios SET estusu='inactivo' WHERE idusu=%s", (user_id,))
    db.commit()
    flash("Usuario desactivado correctamente", "info")
    return redirect(url_for("admin.list_users"))

@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@login_required
@role_required('administrador')
def toggle_user_status(user_id):
    db = current_app.get_db()

    cursor = db.cursor()
    try:
        current_app.logger.info(f"Attempting to toggle status for user_id: {user_id}")
        cursor.execute("SELECT estusu FROM usuarios WHERE idusu = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            current_app.logger.info(f"User found with id {user_id} and status: {user['estusu']}")
            new_status = 'inactivo' if user['estusu'] == 'activo' else 'activo'
            cursor.execute("UPDATE usuarios SET estusu = %s WHERE idusu = %s", (new_status, user_id))
            db.commit()
            flash(f"El estado del usuario ha sido cambiado a {new_status}.", "success")
        else:
            current_app.logger.error(f"No user found with id {user_id}. Query result: {user}")
            flash("Usuario no encontrado.", "error")
    except Exception as e:
        db.rollback()
        flash("Ocurrió un error al cambiar el estado del usuario.", "error")
        current_app.logger.error(f"Error in toggle_user_status: {e}")
    finally:
        cursor.close()

    return redirect(url_for('admin.list_users'))

@admin_bp.route("/categories", methods=["GET"])
@role_required("administrador")
def list_categories():
    db = current_app.get_db()

    cursor = db.cursor()
    cursor.execute("SELECT idcat, tipcat FROM categorias")
    categories = cursor.fetchall()
    return render_template("admin/categories.html", categories=categories)

@admin_bp.route("/categories", methods=["POST"])
@role_required("administrador")
def add_category():
    tipcat = request.form["tipcat"]

    db = current_app.get_db()


    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO categorias (tipcat) VALUES (%s)", (tipcat,))
        db.commit()
        flash("Categoría agregada correctamente", "success")
    except Exception as e:
        db.rollback()
        flash("Error al agregar la categoría: " + str(e), "danger")
    finally:
        cursor.close()

    return redirect(url_for("admin.list_categories"))

@admin_bp.route("/categories/delete/<int:id>", methods=["POST"])
@role_required("administrador")
def delete_category(id):
    db = current_app.get_db()
    cursor = db.cursor()
    
    try:
        # Verificar si la categoría existe
        cursor.execute("SELECT tipcat FROM categorias WHERE idcat = %s", (id,))
        category = cursor.fetchone()
        
        if not category:
            flash("La categoría no existe", "danger")
            return redirect(url_for("admin.list_categories"))
        
        category_name = category[0]
        
        # Verificar si hay productos usando esta categoría
        cursor.execute("SELECT COUNT(*) FROM productos WHERE idcat = %s", (id,))
        count_result = cursor.fetchone()
        product_count = int(count_result[0]) if count_result and count_result[0] is not None else 0
        
        if product_count > 0:
            flash(f'No se puede eliminar la categoría "{category_name}" porque tiene {product_count} producto(s) asociado(s)', "danger")
            return redirect(url_for("admin.list_categories"))
        
        # Eliminar la categoría
        cursor.execute("DELETE FROM categorias WHERE idcat = %s", (id,))
        db.commit()
        flash(f'Categoría "{category_name}" eliminada correctamente', "success")
        
    except Exception as e:
        db.rollback()
        import traceback
        error_msg = f"Error: {str(e)} - Traceback: {traceback.format_exc()}"
        print(error_msg)  # Log en consola
        flash(f"Error al eliminar categoría: {str(e)}", "danger")
    finally:
        cursor.close()
    
    return redirect(url_for("admin.list_categories"))

