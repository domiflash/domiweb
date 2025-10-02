"""
Sistema de Validación de Datos de Entrada para DomiFlash
Centraliza todas las validaciones y sanitización de datos
"""

import re
import html
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import decimal
from werkzeug.security import generate_password_hash

class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass

class InputValidator:
    """Validador centralizado para todos los datos de entrada"""
    
    # Patrones de validación
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^[\+]?[0-9\s\-\(\)]{7,15}$',
        'name': r'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{2,50}$',
        'address': r'^[a-zA-Z0-9À-ÿ\u00f1\u00d1\s\#\-\,\.]{5,200}$',
        'password': r'^.{6,128}$',
        'numeric': r'^[0-9]+$',
        'decimal': r'^[0-9]+(\.[0-9]+)?$',
        'alphanumeric': r'^[a-zA-Z0-9]+$',
        'safe_text': r'^[a-zA-Z0-9À-ÿ\u00f1\u00d1\s\.\,\!\?\-]{1,500}$'
    }
    
    # Caracteres peligrosos
    DANGEROUS_CHARS = ['<', '>', '"', "'", '&', 'script', 'javascript:', 'onload=', 'onerror=']
    
    @classmethod
    def sanitize_input(cls, value: Any) -> str:
        """Sanitiza un input eliminando caracteres peligrosos"""
        if value is None:
            return ""
        
        # Convertir a string
        str_value = str(value).strip()
        
        # Escapar HTML
        str_value = html.escape(str_value)
        
        # Remover caracteres potencialmente peligrosos
        for dangerous in cls.DANGEROUS_CHARS:
            str_value = str_value.replace(dangerous, '')
        
        return str_value
    
    @classmethod
    def validate_email(cls, email: str) -> Dict[str, Any]:
        """Valida formato de email"""
        if not email:
            return {'valid': False, 'error': 'Email es requerido'}
        
        email = cls.sanitize_input(email).lower()
        
        if len(email) > 100:
            return {'valid': False, 'error': 'Email demasiado largo (máximo 100 caracteres)'}
        
        if not re.match(cls.PATTERNS['email'], email):
            return {'valid': False, 'error': 'Formato de email inválido'}
        
        return {'valid': True, 'value': email}
    
    @classmethod
    def validate_password(cls, password: str, confirm_password: str = None) -> Dict[str, Any]:
        """Valida fortaleza de contraseña"""
        if not password:
            return {'valid': False, 'error': 'Contraseña es requerida'}
        
        # No sanitizar la contraseña, solo validar
        if len(password) < 6:
            return {'valid': False, 'error': 'Contraseña debe tener al menos 6 caracteres'}
        
        if len(password) > 128:
            return {'valid': False, 'error': 'Contraseña demasiado larga (máximo 128 caracteres)'}
        
        # Validar fortaleza
        strength_errors = []
        
        if not re.search(r'[A-Z]', password):
            strength_errors.append('al menos una mayúscula')
        
        if not re.search(r'[a-z]', password):
            strength_errors.append('al menos una minúscula')
        
        if not re.search(r'[0-9]', password):
            strength_errors.append('al menos un número')
        
        # Verificar confirmación si se proporciona
        if confirm_password is not None and password != confirm_password:
            return {'valid': False, 'error': 'Las contraseñas no coinciden'}
        
        # Solo advertir sobre fortaleza, no fallar
        warnings = []
        if strength_errors:
            warnings.append(f"Para mayor seguridad, incluye: {', '.join(strength_errors)}")
        
        return {
            'valid': True, 
            'value': password,
            'warnings': warnings
        }
    
    @classmethod
    def validate_name(cls, name: str, field_name: str = "Nombre") -> Dict[str, Any]:
        """Valida nombres de persona, restaurante, etc."""
        if not name:
            return {'valid': False, 'error': f'{field_name} es requerido'}
        
        name = cls.sanitize_input(name)
        
        if len(name) < 2:
            return {'valid': False, 'error': f'{field_name} debe tener al menos 2 caracteres'}
        
        if len(name) > 100:
            return {'valid': False, 'error': f'{field_name} demasiado largo (máximo 100 caracteres)'}
        
        if not re.match(cls.PATTERNS['name'], name):
            return {'valid': False, 'error': f'{field_name} contiene caracteres no válidos'}
        
        return {'valid': True, 'value': name}
    
    @classmethod
    def validate_address(cls, address: str) -> Dict[str, Any]:
        """Valida direcciones"""
        if not address:
            return {'valid': False, 'error': 'Dirección es requerida'}
        
        address = cls.sanitize_input(address)
        
        if len(address) < 5:
            return {'valid': False, 'error': 'Dirección debe tener al menos 5 caracteres'}
        
        if len(address) > 200:
            return {'valid': False, 'error': 'Dirección demasiado larga (máximo 200 caracteres)'}
        
        if not re.match(cls.PATTERNS['address'], address):
            return {'valid': False, 'error': 'Dirección contiene caracteres no válidos'}
        
        return {'valid': True, 'value': address}
    
    @classmethod
    def validate_phone(cls, phone: str) -> Dict[str, Any]:
        """Valida números de teléfono"""
        if not phone:
            return {'valid': False, 'error': 'Teléfono es requerido'}
        
        phone = cls.sanitize_input(phone)
        
        if not re.match(cls.PATTERNS['phone'], phone):
            return {'valid': False, 'error': 'Formato de teléfono inválido'}
        
        return {'valid': True, 'value': phone}
    
    @classmethod
    def validate_price(cls, price: Union[str, float, int]) -> Dict[str, Any]:
        """Valida precios monetarios"""
        if price is None or price == "":
            return {'valid': False, 'error': 'Precio es requerido'}
        
        try:
            # Convertir a decimal para evitar problemas de float
            price_decimal = decimal.Decimal(str(price))
            
            if price_decimal < 0:
                return {'valid': False, 'error': 'Precio no puede ser negativo'}
            
            if price_decimal > 999999:
                return {'valid': False, 'error': 'Precio demasiado alto (máximo $999,999)'}
            
            # Validar que tenga máximo 2 decimales
            if price_decimal.as_tuple().exponent < -2:
                return {'valid': False, 'error': 'Precio no puede tener más de 2 decimales'}
            
            return {'valid': True, 'value': float(price_decimal)}
            
        except (ValueError, decimal.InvalidOperation):
            return {'valid': False, 'error': 'Precio debe ser un número válido'}
    
    @classmethod
    def validate_quantity(cls, quantity: Union[str, int]) -> Dict[str, Any]:
        """Valida cantidades de productos"""
        if quantity is None or quantity == "":
            return {'valid': False, 'error': 'Cantidad es requerida'}
        
        try:
            qty = int(quantity)
            
            if qty < 1:
                return {'valid': False, 'error': 'Cantidad debe ser al menos 1'}
            
            if qty > 100:
                return {'valid': False, 'error': 'Cantidad máxima es 100'}
            
            return {'valid': True, 'value': qty}
            
        except ValueError:
            return {'valid': False, 'error': 'Cantidad debe ser un número entero'}
    
    @classmethod
    def validate_description(cls, description: str, max_length: int = 500) -> Dict[str, Any]:
        """Valida descripciones de productos, restaurantes, etc."""
        if not description:
            description = ""  # Descripción puede ser vacía
        
        description = cls.sanitize_input(description)
        
        if len(description) > max_length:
            return {'valid': False, 'error': f'Descripción demasiado larga (máximo {max_length} caracteres)'}
        
        if description and not re.match(cls.PATTERNS['safe_text'], description):
            return {'valid': False, 'error': 'Descripción contiene caracteres no válidos'}
        
        return {'valid': True, 'value': description}
    
    @classmethod
    def validate_role(cls, role: str) -> Dict[str, Any]:
        """Valida roles de usuario"""
        valid_roles = ['cliente', 'restaurante', 'repartidor', 'administrador']
        
        if not role:
            return {'valid': False, 'error': 'Rol es requerido'}
        
        role = cls.sanitize_input(role).lower()
        
        if role not in valid_roles:
            return {'valid': False, 'error': f'Rol inválido. Valores permitidos: {", ".join(valid_roles)}'}
        
        return {'valid': True, 'value': role}
    
    @classmethod
    def validate_payment_method(cls, method: str) -> Dict[str, Any]:
        """Valida métodos de pago"""
        valid_methods = ['efectivo', 'tarjeta', 'nequi', 'daviplata', 'otro']
        
        if not method:
            return {'valid': False, 'error': 'Método de pago es requerido'}
        
        method = cls.sanitize_input(method).lower()
        
        if method not in valid_methods:
            return {'valid': False, 'error': f'Método de pago inválido. Valores permitidos: {", ".join(valid_methods)}'}
        
        return {'valid': True, 'value': method}
    
    @classmethod
    def validate_order_status(cls, status: str) -> Dict[str, Any]:
        """Valida estados de pedido"""
        valid_statuses = ['pendiente', 'aceptado', 'preparando', 'en_camino', 'entregado', 'cancelado']
        
        if not status:
            return {'valid': False, 'error': 'Estado es requerido'}
        
        status = cls.sanitize_input(status).lower()
        
        if status not in valid_statuses:
            return {'valid': False, 'error': f'Estado inválido. Valores permitidos: {", ".join(valid_statuses)}'}
        
        return {'valid': True, 'value': status}
    
    @classmethod
    def validate_form_data(cls, data: Dict[str, Any], validation_rules: Dict[str, str]) -> Dict[str, Any]:
        """Valida un formulario completo basado en reglas"""
        results = {
            'valid': True,
            'errors': {},
            'values': {},
            'warnings': []
        }
        
        for field, rule in validation_rules.items():
            value = data.get(field)
            
            if rule == 'email':
                result = cls.validate_email(value)
            elif rule == 'password':
                confirm_field = f"{field}_confirm"
                confirm_value = data.get(confirm_field)
                result = cls.validate_password(value, confirm_value)
            elif rule == 'name':
                result = cls.validate_name(value, field.title())
            elif rule == 'address':
                result = cls.validate_address(value)
            elif rule == 'phone':
                result = cls.validate_phone(value)
            elif rule == 'price':
                result = cls.validate_price(value)
            elif rule == 'quantity':
                result = cls.validate_quantity(value)
            elif rule == 'description':
                result = cls.validate_description(value)
            elif rule == 'role':
                result = cls.validate_role(value)
            elif rule == 'payment_method':
                result = cls.validate_payment_method(value)
            elif rule == 'order_status':
                result = cls.validate_order_status(value)
            else:
                # Validación básica por defecto
                result = {'valid': True, 'value': cls.sanitize_input(value)}
            
            if result['valid']:
                results['values'][field] = result['value']
                if 'warnings' in result:
                    results['warnings'].extend(result['warnings'])
            else:
                results['valid'] = False
                results['errors'][field] = result['error']
        
        return results

# Instancia global del validador
input_validator = InputValidator()