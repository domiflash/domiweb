"""
Decorador para validación automática de formularios
"""

from functools import wraps
from flask import request, flash, redirect, url_for, jsonify
from utils.input_validator import input_validator

def validate_form(validation_rules):
    """
    Decorador para validar automáticamente los datos de formularios
    
    Args:
        validation_rules (dict): Diccionario con las reglas de validación
                                Ejemplo: {'email': 'email', 'password': 'password'}
    
    Usage:
        @validate_form({'email': 'email', 'password': 'password'})
        def login():
            # Los datos validados están en request.validated_data
            email = request.validated_data['email']
            password = request.validated_data['password']
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                # Obtener datos del formulario
                form_data = {}
                
                # Combinar datos de form y JSON
                if request.is_json:
                    form_data.update(request.get_json() or {})
                else:
                    form_data.update(request.form.to_dict())
                
                # Validar los datos
                validation_result = input_validator.validate_form_data(form_data, validation_rules)
                
                if not validation_result['valid']:
                    # Si hay errores de validación
                    error_messages = []
                    for field, error in validation_result['errors'].items():
                        error_messages.append(f"{field.replace('_', ' ').title()}: {error}")
                    
                    # Manejar según el tipo de request
                    if request.is_json:
                        return jsonify({
                            'success': False,
                            'errors': validation_result['errors'],
                            'message': 'Errores de validación'
                        }), 400
                    else:
                        # Flash todos los errores
                        for msg in error_messages:
                            flash(f"❌ {msg}", "error")
                        
                        # Intentar redirigir a la página anterior
                        referrer = request.referrer
                        if referrer:
                            return redirect(referrer)
                        else:
                            return redirect(url_for('index'))
                
                # Si hay advertencias, mostrarlas
                if validation_result['warnings']:
                    for warning in validation_result['warnings']:
                        flash(f"⚠️ {warning}", "warning")
                
                # Agregar datos validados al request
                request.validated_data = validation_result['values']
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_json_api(validation_rules):
    """
    Decorador específico para APIs JSON
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                # Solo manejar JSON
                if not request.is_json:
                    return jsonify({
                        'success': False,
                        'message': 'Content-Type debe ser application/json'
                    }), 400
                
                form_data = request.get_json() or {}
                
                # Validar los datos
                validation_result = input_validator.validate_form_data(form_data, validation_rules)
                
                if not validation_result['valid']:
                    return jsonify({
                        'success': False,
                        'errors': validation_result['errors'],
                        'message': 'Errores de validación'
                    }), 400
                
                # Agregar datos validados al request
                request.validated_data = validation_result['values']
                
                # Agregar advertencias si las hay
                if validation_result['warnings']:
                    request.validation_warnings = validation_result['warnings']
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_fields(*required_fields):
    """
    Decorador para requerir campos específicos
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                # Obtener datos
                if request.is_json:
                    data = request.get_json() or {}
                else:
                    data = request.form.to_dict()
                
                # Verificar campos requeridos
                missing_fields = []
                for field in required_fields:
                    if field not in data or not data[field]:
                        missing_fields.append(field.replace('_', ' ').title())
                
                if missing_fields:
                    error_msg = f"Campos requeridos faltantes: {', '.join(missing_fields)}"
                    
                    if request.is_json:
                        return jsonify({
                            'success': False,
                            'message': error_msg,
                            'missing_fields': missing_fields
                        }), 400
                    else:
                        flash(f"❌ {error_msg}", "error")
                        if request.referrer:
                            return redirect(request.referrer)
                        else:
                            return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator