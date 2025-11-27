"""
Rutas de configuración de perfil con validaciones
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from utils.auth_helpers import login_required
from utils.validation_decorators import validate_form
from utils.input_validator import input_validator
from utils.session_manager import require_active_session
from werkzeug.security import generate_password_hash, check_password_hash

config_bp = Blueprint("config", __name__)

@config_bp.route("/profile", methods=["GET", "POST"])
@login_required
@validate_form({
    'nombre': 'name',
    'direccion': 'address',
    'telefono': 'phone'
})
def update_profile():
    """Actualizar perfil de usuario con validaciones"""
    usuario_id = session.get("usuario_id")
    
    if request.method == "POST":
        # Los datos ya están validados por el decorador
        nombre = request.validated_data["nombre"]
        direccion = request.validated_data["direccion"]
        telefono = request.validated_data.get("telefono", "")
        
        try:
            db = current_app.get_db()

            cursor = db.cursor()
            
            # Actualizar datos del usuario
            cursor.execute("""
                UPDATE usuarios 
                SET nomusu = %s, dirusu = %s 
                WHERE idusu = %s
            """, (nombre, direccion, usuario_id))
            
            # Si es restaurante, actualizar también la tabla restaurantes
            if session.get("rol") == "restaurante":
                cursor.execute("""
                    UPDATE restaurantes 
                    SET nomres = %s, dirres = %s, telres = %s 
                    WHERE idusu = %s
                """, (nombre, direccion, telefono, usuario_id))
            
            db.commit()
            cursor.close()
            
            flash("✅ Perfil actualizado exitosamente", "success")
            return redirect(url_for("config.update_profile"))
            
        except Exception as e:
            flash(f"❌ Error al actualizar perfil: {str(e)}", "error")
    
    # Cargar datos actuales del usuario
    db = current_app.get_db()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE idusu = %s", (usuario_id,))
    user_data = cursor.fetchone()
    
    # Si es restaurante, cargar datos adicionales
    restaurant_data = None
    if session.get("rol") == "restaurante":
        cursor.execute("SELECT * FROM restaurantes WHERE idusu = %s", (usuario_id,))
        restaurant_data = cursor.fetchone()
    
    cursor.close()
    
    return render_template("config/profile.html", 
                         user=user_data, 
                         restaurant=restaurant_data)

@config_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Cambiar contraseña con validaciones robustas"""
    usuario_id = session.get("usuario_id")
    
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validar contraseña actual
        if not current_password:
            flash("❌ Contraseña actual es requerida", "error")
            return render_template("config/change_password.html")
        
        # Verificar contraseña actual
        db = current_app.get_db()

        cursor = db.cursor()
        cursor.execute("SELECT conusu FROM usuarios WHERE idusu = %s", (usuario_id,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user["conusu"], current_password):
            flash("❌ Contraseña actual incorrecta", "error")
            cursor.close()
            return render_template("config/change_password.html")
        
        # Validar nueva contraseña
        password_validation = input_validator.validate_password(new_password, confirm_password)
        
        if not password_validation['valid']:
            flash(f"❌ {password_validation['error']}", "error")
            cursor.close()
            return render_template("config/change_password.html")
        
        # Mostrar advertencias si las hay
        if 'warnings' in password_validation:
            for warning in password_validation['warnings']:
                flash(f"⚠️ {warning}", "warning")
        
        try:
            # Actualizar contraseña
            new_password_hash = generate_password_hash(new_password)
            cursor.execute("""
                UPDATE usuarios 
                SET conusu = %s 
                WHERE idusu = %s
            """, (new_password_hash, usuario_id))
            
            db.commit()
            cursor.close()
            
            flash("✅ Contraseña cambiada exitosamente", "success")
            return redirect(url_for("auth.role_dashboard"))
            
        except Exception as e:
            flash(f"❌ Error al cambiar contraseña: {str(e)}", "error")
    
    return render_template("config/change_password.html")

@config_bp.route('/test-session-timeout')
@require_active_session
def test_session_timeout():
    """
    Página de prueba para el sistema de timeout de sesión
    """
    return render_template('config/test_session_timeout.html')


@config_bp.route('/test-validation')
def test_validation():
    """Página de prueba para el sistema de validaciones"""
    if request.method == "POST":
        # Obtener todos los datos del formulario
        form_data = request.form.to_dict()
        
        # Definir reglas de validación
        validation_rules = {
            'email': 'email',
            'password': 'password',
            'name': 'name',
            'address': 'address',
            'phone': 'phone',
            'price': 'price',
            'quantity': 'quantity',
            'description': 'description'
        }
        
        # Validar todos los campos
        results = input_validator.validate_form_data(form_data, validation_rules)
        
        # Mostrar resultados
        if results['valid']:
            flash("✅ Todos los datos son válidos", "success")
            for field, value in results['values'].items():
                flash(f"✓ {field}: {value}", "info")
        else:
            flash("❌ Errores de validación encontrados:", "error")
            for field, error in results['errors'].items():
                flash(f"✗ {field}: {error}", "error")
        
        if results['warnings']:
            for warning in results['warnings']:
                flash(f"⚠️ {warning}", "warning")
    
    return render_template("config/test_validation.html")