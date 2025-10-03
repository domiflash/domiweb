@echo off
echo 📊 EXPORTANDO BASE DE DATOS DOMIFLASH...
echo.

REM Solicitar credenciales de MySQL
set /p mysql_user="Ingresa tu usuario de MySQL (por defecto 'root'): "
if "%mysql_user%"=="" set mysql_user=root

echo.
echo 🔄 Exportando base de datos 'dbflash'...
mysqldump -u %mysql_user% -p dbflash > dbflash_backup.sql

if %errorlevel% equ 0 (
    echo ✅ Base de datos exportada exitosamente como 'dbflash_backup.sql'
    echo.
    echo 📦 ARCHIVOS LISTOS PARA DESPLIEGUE:
    echo    - dbflash_backup.sql (base de datos)
    echo    - Carpeta completa del proyecto
    echo    - .env.deploy-template (plantilla de configuración)
    echo.
    echo 🎯 Ahora puedes comprimir todo y llevarlo a otra máquina!
) else (
    echo ❌ Error al exportar la base de datos
    echo Verifica que MySQL esté ejecutándose y las credenciales sean correctas
)

echo.
pause