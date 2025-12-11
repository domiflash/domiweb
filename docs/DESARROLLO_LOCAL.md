# 🚀 Guía de Comandos - Desarrollo Local DomiFlash

## 📋 **RESUMEN RÁPIDO**

### ¿Qué bases de datos existen?

1. **🌐 Render (Producción)** - La que usa tu app desplegada
   - URL: `postgresql://usuario:pass@host.render.com/dbflash`
   - **NO modificar** durante desarrollo
   - Solo para producción

2. **💻 Local (Desarrollo)** - En tu PC
   - Para probar cambios SIN afectar producción
   - Necesitas PostgreSQL instalado
   - **Totalmente independiente de Render**

---

## ✅ **COMANDOS PARA DESARROLLO LOCAL**

### 1. Activar Entorno Virtual

```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Deberías ver (venv) al inicio de tu terminal
# (venv) PS C:\Users\braya\Documents\VS CODE\domiweb>

# Verificar Python
python --version
# Debería mostrar: Python 3.13.3
```

### 2. Verificar Dependencias Instaladas

```powershell
# Ver paquetes instalados
pip list

# Si falta algo, instalar todas las dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos Local

**IMPORTANTE:** Tienes 2 opciones aquí

#### **Opción A: PostgreSQL Local (Recomendado para desarrollo)**

```powershell
# 1. Verificar si PostgreSQL está instalado
psql --version

# Si no está instalado, descargar de:
# https://www.postgresql.org/download/windows/
# O instalar con Chocolatey:
choco install postgresql

# 2. Crear usuario y base de datos
# Abrir SQL Shell (psql) o pgAdmin

# En psql:
CREATE DATABASE dbflash;
CREATE USER domiflash WITH PASSWORD 'tu_password_local';
GRANT ALL PRIVILEGES ON DATABASE dbflash TO domiflash;

# 3. Actualizar .env con configuración PostgreSQL local
# (ver siguiente sección)
```

#### **Opción B: Usar BD de Render (NO RECOMENDADO para desarrollo)**

```powershell
# Solo para pruebas rápidas, NO para desarrollo normal
# Actualiza .env con las credenciales de Render
# RIESGO: Cualquier cambio afecta producción
```

### 4. Actualizar Archivo `.env`

**Para PostgreSQL Local (RECOMENDADO):**

```env
# 🗄️ === CONFIGURACIÓN DE BASE DE DATOS ===
DB_HOST=localhost
DB_PORT=5432
DB_USER=domiflash
DB_PASSWORD=tu_password_local_aqui
DB_NAME=dbflash

# 🔐 === SEGURIDAD DE FLASK ===
SECRET_KEY=clave_super_secreta_de_desarrollo_local

# 📧 === EMAIL (Opcional para desarrollo local) ===
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password_gmail
MAIL_DEFAULT_SENDER=tu_email@gmail.com

# 🕐 === SESIONES ===
SESSION_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
```

### 5. Crear Esquema de Base de Datos Local

```powershell
# Opción 1: Desde pgAdmin
# - Conectar a tu PostgreSQL local (localhost:5432)
# - Abrir Query Tool
# - Copiar contenido de database/dbflash_postgresql.sql
# - Ejecutar (F5)

# Opción 2: Desde psql (terminal)
psql -U domiflash -d dbflash -f database/dbflash_postgresql.sql

# Debería crear: 12 tablas, 21 procedimientos, 8 funciones, 3 triggers
```

### 6. (Opcional) Insertar Datos Demo

```powershell
# Para tener datos de ejemplo para probar

# Opción 1: Desde pgAdmin
# - Abrir database/insert_data_demo.sql
# - IMPORTANTE: Primero generar hashes reales (ver sección siguiente)
# - Ejecutar el script

# Opción 2: Desde psql
psql -U domiflash -d dbflash -f database/insert_data_demo.sql
```

**⚠️ IMPORTANTE sobre insert_data_demo.sql:**

Los hashes de contraseña son ejemplos. Para login real:

```powershell
# Ejecutar en Python (con venv activado)
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('1234'))"

# Copiar el hash generado y reemplazarlo en insert_data_demo.sql
# en los INSERT de usuarios
```

### 7. Crear Usuario Administrador Local

```powershell
# Generar hash para contraseña
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"

# Copiar el hash y ejecutar en PostgreSQL:
```

```sql
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu)
VALUES (
    'Administrador Local',
    'admin@local.com',
    'EL_HASH_GENERADO_AQUI',  -- Reemplazar con el hash
    'Calle Local 123',
    '3001234567',
    'administrador',
    'activo'
);

-- Verificar
SELECT idusu, nomusu, corusu, rolusu FROM usuarios WHERE rolusu = 'administrador';
```

### 8. Iniciar Servidor de Desarrollo

```powershell
# Asegúrate de estar en la carpeta del proyecto
cd C:\Users\braya\Documents\VS CODE\domiweb

# Con entorno virtual activado
python app.py

# Deberías ver:
# * Running on http://127.0.0.1:5000
# * Debug mode: on (o off, dependiendo de config)
```

### 9. Abrir en Navegador

```
http://localhost:5000
```

**Rutas principales:**
- `/` - Página principal
- `/auth/login` - Login
- `/auth/register` - Registro
- `/admin/dashboard` - Panel administrador (login requerido)
- `/cliente/menu` - Menú de productos
- `/restaurante/pedidos` - Pedidos restaurante
- `/repartidor/dashboard` - Dashboard repartidor

### 10. Detener el Servidor

```
Ctrl + C en la terminal
```

### 11. Desactivar Entorno Virtual (cuando termines)

```powershell
deactivate
```

---

## 🔍 **COMANDOS DE VERIFICACIÓN**

### Verificar Estado de Git

```powershell
git status
git branch
git log --oneline -5
```

### Verificar Conexión a BD

```powershell
# Ejecutar script de verificación
python verify_db.py  # Si aún existe

# O crear uno nuevo temporal:
python -c "import psycopg; from config import DB_CONFIG; conn = psycopg.connect(**DB_CONFIG); print('✅ Conexión exitosa'); conn.close()"
```

### Ver Logs de la Aplicación

```powershell
# Si configuraste logging
Get-Content logs/app.log -Tail 50

# O ver en tiempo real
Get-Content logs/app.log -Wait
```

---

## 🐛 **SOLUCIÓN DE PROBLEMAS COMUNES**

### Error: "No module named 'psycopg'"

```powershell
pip install psycopg[binary]
```

### Error: "Unable to connect to database"

```powershell
# Verificar que PostgreSQL esté corriendo
Get-Service -Name postgresql*

# Iniciar PostgreSQL si está detenido
Start-Service postgresql-x64-15  # Ajustar nombre según tu versión

# Verificar credenciales en .env
```

### Error: "SECRET_KEY not found"

```powershell
# Asegúrate de tener .env en la raíz del proyecto
# Si no existe, copia .env.example:
Copy-Item .env.example .env

# Genera una SECRET_KEY segura:
python -c "import secrets; print(secrets.token_hex(32))"
# Copia el resultado y pégalo en .env
```

### Error: "No such table/relation"

```powershell
# Ejecutar el esquema de BD
psql -U domiflash -d dbflash -f database/dbflash_postgresql.sql
```

---

## 📊 **WORKFLOW COMPLETO DE DESARROLLO**

### Día a día:

```powershell
# 1. Activar entorno
.\venv\Scripts\Activate.ps1

# 2. Actualizar código desde Git
git pull origin main

# 3. Instalar dependencias (si hay cambios)
pip install -r requirements.txt

# 4. Iniciar servidor
python app.py

# 5. Desarrollar y probar en http://localhost:5000

# 6. Hacer cambios, commit y push
git add .
git commit -m "Tu mensaje"
git push

# 7. Desactivar entorno al terminar
deactivate
```

---

## 🔄 **DIFERENCIA: LOCAL vs PRODUCCIÓN**

| Aspecto | Local (Tu PC) | Render (Producción) |
|---------|---------------|---------------------|
| **Base de Datos** | PostgreSQL localhost | PostgreSQL Render Cloud |
| **Datos** | Independientes | Datos reales de producción |
| **Cambios** | Solo afectan tu PC | Afectan a todos los usuarios |
| **Servidor** | `python app.py` | Gunicorn automático |
| **URL** | http://localhost:5000 | https://domiweb-xxx.onrender.com |
| **Logs** | Terminal local | Dashboard de Render |
| **Email** | Opcional | Configurado |

**🔴 IMPORTANTE:** Los cambios en local **NO afectan** producción hasta que hagas deploy (push a main y Render actualiza automáticamente)

---

## ✅ **CHECKLIST ANTES DE EMPEZAR**

- [ ] Entorno virtual activado (`.\venv\Scripts\Activate.ps1`)
- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `dbflash` creada
- [ ] Usuario `domiflash` creado en PostgreSQL
- [ ] Archivo `.env` configurado con credenciales locales
- [ ] Esquema de BD ejecutado (`dbflash_postgresql.sql`)
- [ ] Usuario admin creado en BD local
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Servidor iniciado (`python app.py`)
- [ ] Navegador abierto en `http://localhost:5000`

---

## 🎯 **RESUMEN DE COMANDOS MÁS USADOS**

```powershell
# ACTIVAR ENTORNO
.\venv\Scripts\Activate.ps1

# INICIAR SERVIDOR
python app.py

# VER ESTADO GIT
git status

# INSTALAR DEPENDENCIAS
pip install -r requirements.txt

# GENERAR HASH PASSWORD
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('tu_password'))"

# DESACTIVAR ENTORNO
deactivate
```

---

**¿Tienes PostgreSQL instalado localmente?** Si no, puedo guiarte en la instalación paso a paso.
