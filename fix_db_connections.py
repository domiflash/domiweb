#!/usr/bin/env python3
"""
Script para reemplazar current_app.db por current_app.get_db() en todo el proyecto
"""

import re
from pathlib import Path

# Archivos a procesar
files_to_process = [
    'routes/admin.py',
    'routes/cliente.py',
    'routes/config.py',
    'routes/repartidor.py',
    'routes/restaurante.py',
    'utils/delivery_calculator.py',
]

def fix_db_access(file_path):
    """Reemplazar current_app.db por current_app.get_db()"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Buscar patrones donde se usa current_app.db.cursor()
    # y reemplazar con db = current_app.get_db(); cursor = db.cursor()
    
    # Patrón 1: cursor = current_app.db.cursor()
    content = re.sub(
        r'(\s+)cursor = current_app\.db\.cursor\(\)',
        r'\1db = current_app.get_db()\n\1cursor = db.cursor()',
        content
    )
    
    # Patrón 2: current_app.db.commit() -> db.commit() (si existe db = current_app.get_db() antes)
    # Esto requiere más lógica, mejor hacerlo manualmente o en un segundo paso
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Actualizado: {file_path}')
        return True
    else:
        print(f'⏭️  Sin cambios: {file_path}')
        return False

def main():
    print('🔧 Actualizando archivos para usar get_db()...\n')
    
    updated_count = 0
    for file_path in files_to_process:
        if Path(file_path).exists():
            if fix_db_access(file_path):
                updated_count += 1
        else:
            print(f'❌ No encontrado: {file_path}')
    
    print(f'\n✨ Proceso completado. {updated_count} archivos actualizados.')

if __name__ == '__main__':
    main()
