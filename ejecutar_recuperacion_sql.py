"""
Script para ejecutar automáticamente el SQL de recuperación de contraseña
"""

import mysql.connector
from config import DB_CONFIG

def ejecutar_script_recuperacion():
    """Ejecuta el script SQL de recuperación de contraseña"""
    
    # Leer el script SQL
    with open('scripts/implementar_recuperacion_password.sql', 'r', encoding='utf-8') as file:
        script_content = file.read()
    
    # Dividir en comandos individuales
    comandos = []
    comando_actual = ""
    en_delimitador = False
    
    for linea in script_content.split('\n'):
        linea = linea.strip()
        
        # Saltar comentarios y líneas vacías
        if not linea or linea.startswith('--'):
            continue
            
        # Manejar USE dbflash;
        if linea.startswith('USE '):
            continue
            
        # Manejar DELIMITER
        if linea.startswith('DELIMITER'):
            if '//':
                en_delimitador = True
            else:
                en_delimitador = False
            continue
            
        comando_actual += linea + "\n"
        
        # Determinar fin de comando
        if en_delimitador:
            if linea.endswith('//'):
                comandos.append(comando_actual.replace('//', '').strip())
                comando_actual = ""
        else:
            if linea.endswith(';'):
                comandos.append(comando_actual.strip())
                comando_actual = ""
    
    # Conectar a la base de datos
    print("🔗 Conectando a la base de datos...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Ejecutar comandos
    ejecutados = 0
    errores = 0
    
    for i, comando in enumerate(comandos):
        if not comando.strip():
            continue
            
        try:
            print(f"📝 Ejecutando comando {i+1}/{len(comandos)}...")
            
            # Para procedimientos, usar multi=True
            if 'CREATE PROCEDURE' in comando or 'CREATE TABLE' in comando:
                for result in cursor.execute(comando, multi=True):
                    pass
            else:
                cursor.execute(comando)
            
            conn.commit()
            ejecutados += 1
            print(f"✅ Comando {i+1} ejecutado exitosamente")
            
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg or "Duplicate" in error_msg:
                print(f"⚠️ Comando {i+1}: Ya existe (omitido)")
            else:
                print(f"❌ Error en comando {i+1}: {error_msg}")
                errores += 1
    
    cursor.close()
    conn.close()
    
    print(f"\n🎉 Script ejecutado:")
    print(f"   ✅ Exitosos: {ejecutados}")
    print(f"   ❌ Errores: {errores}")
    print(f"   📋 Total: {len(comandos)}")
    
    if errores == 0:
        print("\n🚀 ¡Sistema de recuperación de contraseña listo!")
    else:
        print(f"\n⚠️ Algunos comandos fallaron, pero el sistema debería funcionar")

if __name__ == "__main__":
    try:
        ejecutar_script_recuperacion()
    except Exception as e:
        print(f"💥 Error ejecutando script: {e}")
        print("\n📝 Intenta ejecutar manualmente el contenido de:")
        print("   scripts/implementar_recuperacion_password.sql")
        print("   en tu cliente MySQL (phpMyAdmin, etc.)")