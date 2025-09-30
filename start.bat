@echo off
echo 🚀 Iniciando domiweb

:: Actualiza pip y librerías
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt

:: Define modo
if "%1"=="prod" (
    set FLASK_ENV=production
) else (
    set FLASK_ENV=development
)

:: Ejecuta la app
python app.py
pause
