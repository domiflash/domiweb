# 📦 GUÍA DE DESPLIEGUE - DOMIFLASH
# Archivos esenciales para llevar y configurar en otra máquina

## 🗂️ ARCHIVOS OBLIGATORIOS A INCLUIR:

### 📄 Configuración Base
- `.env` (con configuración de base de datos)
- `requirements.txt` (dependencias Python)
- `install.bat` (script de instalación automática)
- `start.bat` (script para ejecutar la aplicación)

### 📊 Base de Datos
- `dbflash.sql` (archivo de backup completo de la base de datos)
- `scripts/` (todos los scripts SQL de recuperación de contraseñas)

### 🐍 Código Fuente
- Todos los archivos `.py` del proyecto
- Carpeta `templates/` completa
- Carpeta `static/` completa  
- Carpeta `models/` completa
- Carpeta `routes/` completa
- Carpeta `utils/` completa

### 📚 Documentación
- `README.md` (guía completa de instalación)
- `PRESENTACION.md` (guía para la presentación)
- `docs/` (documentación técnica completa)

### ⚙️ Archivos de Sistema
- `app.py` (aplicación principal)
- `config.py` (configuración)

## 🚀 PASOS DE INSTALACIÓN EN NUEVA MÁQUINA:

1. Descomprimir la carpeta
2. Instalar Python 3.8+ y MySQL/MariaDB
3. Ejecutar `install.bat` (instala todo automáticamente)
4. Importar `dbflash.sql` en MySQL
5. Ajustar `.env` con credenciales locales si es necesario
6. Ejecutar `start.bat` para iniciar la aplicación

## 🎯 ESTRUCTURA FINAL RECOMENDADA:
```
DomiFlash-Deploy/
├── domiweb/                 # Código completo del proyecto
├── dbflash.sql             # Backup de base de datos
├── INSTRUCCIONES.md        # Esta guía
└── README-DEPLOY.txt       # Instrucciones rápidas
```

## 📋 CHECKLIST PRE-PRESENTACIÓN:
- [ ] Carpeta comprimida creada
- [ ] Base de datos exportada
- [ ] .env configurado
- [ ] Scripts de instalación probados
- [ ] Documentación incluida
- [ ] Backup del proyecto completo

## 🔧 CONFIGURACIONES IMPORTANTES:
- Puerto por defecto: 5000
- Base de datos: dbflash
- Usuario admin: admin@domiflash / 123456789
- Roles disponibles: cliente, restaurante, repartidor, administrador