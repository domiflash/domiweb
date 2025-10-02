# 📁 Estructura del Proyecto DomiFlash

## 🏗️ Organización de Directorios

```
domiweb/
├── 📂 app.py                 # Aplicación principal Flask
├── 📂 config.py             # Configuración de la aplicación
├── 📂 requirements.txt      # Dependencias de Python
├── 📂 start.bat            # Script de inicio para Windows
├── 📂 README.md            # Documentación principal
├── 📂 .gitignore           # Archivos ignorados por Git
│
├── 📁 models/              # Modelos de datos
│   ├── admin.py
│   ├── cliente.py
│   ├── pagos.py
│   ├── pedidos.py
│   ├── productos.py
│   ├── repartidor.py
│   └── usuarios.py
│
├── 📁 routes/              # Rutas y controladores
│   ├── admin.py
│   ├── auth.py
│   ├── cliente.py
│   ├── repartidor.py
│   └── restaurante.py
│
├── 📁 templates/           # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── 📁 admin/
│   ├── 📁 auth/
│   ├── 📁 cliente/
│   ├── 📁 repartidor/
│   └── 📁 restaurante/
│
├── 📁 static/              # Archivos estáticos
│   ├── 📁 css/
│   ├── 📁 js/
│   ├── 📁 img/
│   ├── 📁 icons/
│   ├── manifest.json
│   └── sw.js
│
├── 📁 utils/               # Utilidades y helpers
│   ├── auth_helpers.py
│   └── delivery_calculator.py
│
├── 📁 docs/                # Documentación del proyecto
│   └── 📁 reportes/        # Reportes de desarrollo (NO se suben a Git)
│
├── 📁 scripts/             # Scripts SQL y utilidades
│   └── fix_detalle_pedidos.sql
│
└── 📁 temp/                # Archivos temporales (NO se suben a Git)
    ├── test_analysis_complete.py
    ├── test_completo_domiweb.py
    └── test_sistema.py
```

## 🚫 Archivos NO incluidos en Git

### Automáticamente Ignorados (.gitignore)
- `venv/` - Entorno virtual de Python
- `__pycache__/` - Archivos compilados de Python
- `.env` - Variables de entorno
- `flask_session/` - Sesiones de Flask
- `logs/` - Archivos de log
- `docs/reportes/` - Reportes de desarrollo
- `temp/` - Archivos temporales
- `*.pyc, *.log, *.tmp` - Archivos temporales

### Razones para Ignorar
- **Seguridad**: `.env` contiene credenciales
- **Tamaño**: `venv/` es muy pesado y se puede recrear
- **Temporal**: `flask_session/` y `logs/` se generan automáticamente
- **Personal**: Reportes son específicos del desarrollo local

## 📋 Archivos de Configuración

### Para Desarrollo Local
- `.env` - Variables de entorno (DB, secretos)
- `venv/` - Entorno virtual con dependencias
- `logs/` - Archivos de logging

### Para Producción
- `requirements.txt` - Lista de dependencias
- `config.py` - Configuración de la aplicación
- `start.bat` - Script de inicio

## 🔧 Instalación y Configuración

### 1. Clonar Repositorio
```bash
git clone https://github.com/domiflash/domiweb.git
cd domiweb
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` con:
```
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=domiweb
SECRET_KEY=tu_clave_secreta
```

### 5. Ejecutar Aplicación
```bash
python app.py
# O usar el script de inicio
start.bat
```

## 📚 Documentación Adicional

- **Reportes de Desarrollo**: `docs/reportes/` (solo local)
- **Scripts de Base de Datos**: `scripts/`
- **Tests**: `temp/` (solo local)

---

*Estructura actualizada: Octubre 2025*