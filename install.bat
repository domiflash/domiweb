@echo off
echo.
echo ==========================================
echo 🍕 DomiFlash - Instalacion Automatica
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instala Python 3.8+ primero.
    echo 📥 Descarga: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado. Por favor instala Git primero.
    echo 📥 Descarga: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git detectado
git --version

echo.
echo 🔧 Iniciando instalación...
echo.

REM Crear ambiente virtual
echo 🐍 Creando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ Error creando ambiente virtual
    pause
    exit /b 1
)

REM Activar ambiente virtual
echo 🔄 Activando ambiente virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

REM Crear archivo .env si no existe
if not exist .env (
    echo ⚙️ Creando archivo de configuración...
    copy .env.example .env
    echo.
    echo 📝 IMPORTANTE: Edita el archivo .env con tu configuración
    echo    - Configura la base de datos
    echo    - Configura el email de Gmail
    echo    - Genera una SECRET_KEY segura
    echo.
)

echo.
echo ==========================================
echo ✅ Instalación completada exitosamente!
echo ==========================================
echo.
echo 📋 Próximos pasos:
echo.
echo 1️⃣  Editar archivo .env con tu configuración
echo 2️⃣  Configurar base de datos MySQL/MariaDB
echo 3️⃣  Ejecutar: start.bat
echo.
echo 🌐 La aplicación estará en: http://127.0.0.1:5000
echo.
echo 📚 Ver README.md para guía completa
echo.
pause