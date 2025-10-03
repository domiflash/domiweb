@echo off
title DomiFlash - Sistema de Delivery

echo.
echo ==========================================
echo 🍕 DomiFlash - Sistema de Delivery
echo ==========================================
echo.

REM Verificar si el ambiente virtual existe
if not exist venv\ (
    echo ❌ Ambiente virtual no encontrado
    echo 🔧 Ejecuta install.bat primero para configurar el proyecto
    pause
    exit /b 1
)

REM Activar ambiente virtual
echo 🔄 Activando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar archivo .env
if not exist .env (
    echo ❌ Archivo .env no encontrado
    echo 📝 Copia .env.example como .env y configura tus variables
    pause
    exit /b 1
)

REM Verificar dependencias
echo 📦 Verificando dependencias...
pip check >nul 2>&1
if errorlevel 1 (
    echo 🔄 Actualizando dependencias...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

REM Configurar modo de ejecución
if "%1"=="prod" (
    echo 🏭 Modo: Producción
    set FLASK_ENV=production
    set FLASK_DEBUG=False
) else (
    echo 🔧 Modo: Desarrollo
    set FLASK_ENV=development
    set FLASK_DEBUG=True
)

echo.
echo 🚀 Iniciando DomiFlash...
echo 🌐 Aplicación disponible en: http://127.0.0.1:5000
echo 🛑 Presiona Ctrl+C para detener
echo.

REM Ejecutar la aplicación
python app.py

echo.
echo 👋 DomiFlash detenido
pause
