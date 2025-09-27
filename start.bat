@echo off
echo 🚀 Iniciando domiweb

:: Actualiza pip y librerías
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt

:: Verifica MySQL
mysqladmin ping >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MySQL/MariaDB no está corriendo. Inicia MySQL antes de continuar.
    pause
    exit /b
)
echo ✅ MySQL/MariaDB activo.

:: Define modo
if "%1"=="prod" (
    set FLASK_ENV=production
) else (
    set FLASK_ENV=development
)

:: Ejecuta la app
python app.py
pause
