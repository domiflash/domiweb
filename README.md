# 🍕 DomiFlash - Sistema de Delivery Completo

**Plataforma web avanzada de gestión de pedidos y delivery** desarrollada con Flask, MySQL y tecnologías modernas.

## 🌟 Características Implementadas

### 🔐 **Seguridad Robusta**
- ✅ **Autenticación multirol** (Admin, Cliente, Restaurante, Repartidor)
- ✅ **Timeout de sesión automático** (30 min con alertas)
- ✅ **Validación de entrada** centralizada (XSS, SQL injection)
- ✅ **Recuperación de contraseña** por email
- ✅ **Límite de intentos de login** con bloqueo temporal
- ✅ **Cookies seguras** (HttpOnly, SameSite)

### � **Funcionalidades de Negocio**
- �🛒 **Carrito de compras** dinámico con AJAX
- 💳 **Múltiples métodos de pago** (Efectivo, Tarjeta, Nequi, Daviplata)
- 🚚 **Gestión completa de repartidores** y tracking
- 📊 **Dashboard administrativo** con estadísticas
- 📱 **Progressive Web App (PWA)** - Instalable
- 🌙 **Dark Mode** completo y persistente

### 🛡️ **Tecnología Avanzada**
- ⚡ **Reconexión automática** de base de datos
- � **Sistema de sesiones** con renovación inteligente
- 📧 **Email automático** (Flask-Mail + Gmail SMTP)
- 🔄 **Validación en tiempo real** con decoradores
- 📱 **Responsive design** con TailwindCSS

---

## 🚀 Instalación Completa (Guía de Presentación)

### 📋 **Prerrequisitos**
- ✅ **Python 3.8+** instalado
- ✅ **MySQL/MariaDB** corriendo
- ✅ **Git** instalado
- ✅ **Cuenta de Gmail** (para emails)

---

### � **Paso 1: Clonar el Repositorio**

```bash
# Clonar el proyecto
git clone https://github.com/domiflash/domiweb.git

# Entrar al directorio
cd domiweb

# Verificar que estás en la rama correcta
git checkout flujos
```

---

### 🐍 **Paso 2: Crear Ambiente Virtual**

```bash
# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

# Verificar activación (debería mostrar (venv) al inicio del prompt)
```

---

### � **Paso 3: Instalar Dependencias**

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

### 🗄️ **Paso 4: Configurar Base de Datos**

#### **4.1 Crear la Base de Datos**
```sql
-- En MySQL/MariaDB:
CREATE DATABASE dbflash CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'domiflash'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON dbflash.* TO 'domiflash'@'localhost';
FLUSH PRIVILEGES;
```

#### **4.2 Ejecutar Scripts SQL**
```bash
# Importar estructura de base de datos (si tienes el archivo .sql)
mysql -u domiflash -p dbflash < database/structure.sql

# O ejecutar los scripts en orden:
mysql -u domiflash -p dbflash < scripts/paso1_tabla_tokens.sql
mysql -u domiflash -p dbflash < scripts/implementar_recuperacion_password.sql
# ... (ejecutar todos los scripts en orden)
```

---

### ⚙️ **Paso 5: Configurar Variables de Entorno**

Crear archivo `.env` en la raíz del proyecto:

```env
# 🗄️ Configuración de Base de Datos
DB_HOST=localhost
DB_USER=domiflash
DB_PASSWORD=tu_password_seguro
DB_NAME=dbflash

# 🔐 Clave secreta de Flask (genera una nueva)
SECRET_KEY=tu_clave_super_secreta_aqui_cambiar

# 📧 Configuración de Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password_gmail
MAIL_DEFAULT_SENDER=tu_email@gmail.com

# 🕐 Configuración de Sesiones
SESSION_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
SESSION_COOKIE_SECURE=False

# 🚫 Límites de Seguridad
MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_TIMEOUT_MINUTES=15
```

---

### 📧 **Paso 6: Configurar Gmail para Emails**

#### **6.1 Habilitar Contraseña de Aplicación**
1. Ve a tu **Cuenta de Google**
2. **Seguridad** → **Verificación en 2 pasos** (activar si no está)
3. **Contraseñas de aplicaciones** → **Generar nueva**
4. Selecciona **"Otra"** → Escribe **"DomiFlash"**
5. **Copia la contraseña generada** (16 caracteres)
6. **Úsala en `MAIL_PASSWORD`** del archivo `.env`

---

### 🧪 **Paso 7: Crear Datos de Prueba**

#### **7.1 Usuario Administrador**
```sql
-- Insertar usuario admin para pruebas
INSERT INTO usuarios (nomusu, corusu, conusu, rolusu, estusu) VALUES 
('Administrador', 'admin@domiflash', 'pbkdf2:sha256:hasheado', 'administrador', 'activo');
```

#### **7.2 Datos de Prueba Rápidos**
```sql
-- Cliente de prueba
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu) VALUES 
('Cliente Test', 'cliente@test.com', 'hash_123', 'Calle 123', 'cliente', 'activo');

-- Restaurante de prueba  
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu) VALUES 
('Restaurante Demo', 'restaurant@test.com', 'hash_123', 'Ave Principal', 'restaurante', 'activo');
```

---

### 🚀 **Paso 8: Ejecutar la Aplicación**

```bash
# Método 1: Desarrollo rápido
python app.py

# Método 2: Con archivo de inicio
.\start.bat

# Método 3: Producción con Waitress
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

**🌐 La aplicación estará disponible en:** `http://127.0.0.1:5000`

---

## 🧪 **Verificación y Pruebas**

### ✅ **Checklist de Funcionamiento**

1. **🔗 Acceso Principal**
   - [ ] Página principal carga correctamente
   - [ ] Dark mode funciona
   - [ ] PWA se puede instalar

2. **� Sistema de Autenticación**
   - [ ] Login: `admin@domiflash` / `123456`
   - [ ] Registro de nuevo usuario
   - [ ] Recuperación de contraseña por email
   - [ ] Timeout de sesión (30 min)

3. **🛡️ Seguridad**
   - [ ] Validación de formularios
   - [ ] Alertas de sesión próxima a expirar
   - [ ] Bloqueo por intentos fallidos
   - [ ] Emails de recuperación

4. **📱 Funcionalidades**
   - [ ] Dashboard por rol
   - [ ] Carrito de compras
   - [ ] Gestión de pedidos
   - [ ] Sistema de pagos

### 🎯 **URLs de Prueba**

```bash
# Principales
http://127.0.0.1:5000/                      # Página principal
http://127.0.0.1:5000/auth/login            # Login
http://127.0.0.1:5000/auth/register         # Registro

# Sistemas de prueba (requiere login)
http://127.0.0.1:5000/config/test-validation      # Prueba validaciones
http://127.0.0.1:5000/config/test-session-timeout # Prueba timeout sesión
http://127.0.0.1:5000/config/update-profile       # Actualizar perfil
```

---

## 🛠️ **Solución de Problemas Comunes**

### ❌ **Error de Base de Datos**
```bash
# Verificar conexión
mysql -u domiflash -p -h localhost

# Verificar que la BD existe
SHOW DATABASES;
USE dbflash;
SHOW TABLES;
```

### ❌ **Error de Dependencias**
```bash
# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### ❌ **Error de Email**
- ✅ Verificar que Gmail tiene **verificación en 2 pasos** activada
- ✅ Usar **contraseña de aplicación**, no la contraseña normal
- ✅ Verificar el archivo `.env` con datos correctos

### ❌ **Error de Puerto**
```bash
# Si el puerto 5000 está ocupado
netstat -ano | findstr :5000
# Cambiar puerto en app.py: app.run(port=5001)
```

---

## 📚 **Estructura de Archivos Importantes**

```
domiweb/
├── 📄 app.py                    # Aplicación principal
├── 📄 config.py                 # Configuraciones
├── 📄 requirements.txt          # Dependencias
├── 📄 .env                      # Variables de entorno (crear)
├── 📄 start.bat                 # Script de inicio Windows
├── 📁 routes/                   # Controladores
│   ├── auth.py                  # Autenticación
│   ├── session.py               # Gestión de sesiones
│   └── config.py                # Configuración de perfil
├── 📁 utils/                    # Utilidades
│   ├── session_manager.py       # Timeout de sesiones
│   ├── input_validator.py       # Validaciones
│   ├── password_recovery.py     # Recuperación contraseñas
│   └── db_helpers.py            # Helpers de BD
├── 📁 templates/                # Plantillas HTML
├── 📁 static/                   # Archivos estáticos
└── 📁 scripts/                  # Scripts SQL
```

---

## 🎯 **Para la Presentación**

### 📋 **Demostración Sugerida**

1. **🚀 Instalación** (5 min)
   - Clonar repositorio
   - Crear ambiente virtual
   - Instalar dependencias

2. **⚙️ Configuración** (5 min)
   - Crear archivo `.env`
   - Configurar base de datos
   - Probar conexión

3. **🔐 Seguridad** (10 min)
   - Login con validaciones flexibles
   - Sistema de timeout de sesión
   - Recuperación de contraseña por email
   - Validación de entrada automática

4. **💼 Funcionalidades** (10 min)
   - Dashboard multirol
   - Carrito de compras
   - Sistema de pedidos
   - PWA e instalación móvil

### 🏆 **Puntos Destacados**

- ✨ **Código limpio** y bien documentado
- 🛡️ **Seguridad implementada** desde el diseño
- 📱 **Tecnologías modernas** (PWA, AJAX, TailwindCSS)
- 🔄 **Sistema robusto** con reconexión automática
- 📧 **Integración completa** de email
- 🕐 **Gestión inteligente** de sesiones

---

## 👨‍💻 **Información del Desarrollador**

- **Proyecto**: Sistema de Delivery DomiFlash
- **Tecnologías**: Flask, MySQL, TailwindCSS, PWA
- **Características**: Seguridad avanzada, timeout de sesión, validaciones
- **Repositorio**: [github.com/domiflash/domiweb](https://github.com/domiflash/domiweb)
- **Rama actual**: `flujos` (con todas las mejoras de seguridad)

---

**🎉 ¡Listo para presentar! La aplicación está completamente funcional y lista para demostración.** 🚀
DB_PASSWORD=tu_password
DB_NAME=domiweb
SECRET_KEY=tu_clave_secreta_muy_segura
```

### 4. **Ejecutar Aplicación**
```bash
python app.py
# O usar el script de Windows
start.bat
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

## 🎯 Funcionalidades por Rol

### 👤 **Cliente**
- Registro y autenticación
- Explorar restaurantes y menús
- Carrito de compras dinámico
- Múltiples métodos de pago
- Historial de pedidos
- Descarga de facturas PDF

### 🍴 **Restaurante**
- Dashboard de pedidos en tiempo real
- Gestión de productos y menús
- Actualización de estados de pedidos
- Visualización de detalles completos

### 🚚 **Repartidor**
- Lista de pedidos asignados
- Actualización de estado de entrega
- Información de cliente y dirección

### 👨‍💼 **Administrador**
- Gestión completa de usuarios
- Estadísticas y reportes
- Configuración del sistema
- Monitoreo de operaciones

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL con PyMySQL
- **Frontend**: HTML5, TailwindCSS, JavaScript ES6+
- **PWA**: Service Workers, Web App Manifest
- **Seguridad**: Flask-Bcrypt, Sessions
- **PDF**: Print API nativa del navegador

## 📱 Características PWA

- ✅ **Instalable** en dispositivos móviles
- ✅ **Funciona offline** (páginas en caché)
- ✅ **Responsive** en todos los dispositivos
- ✅ **Dark mode** persistente

## 🔧 Configuración Avanzada

### Variables de Entorno Disponibles
```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=domiweb

# Seguridad
SECRET_KEY=clave-super-secreta
DEBUG=True

# Opcional
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Scripts de Base de Datos
- `scripts/fix_detalle_pedidos.sql` - Corrige datos de pedidos

## 📋 Comandos Útiles

```bash
# Activar entorno virtual
venv\Scripts\activate

# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Verificar estructura del proyecto
tree /f /a

# Limpiar caché de Python
find . -type d -name "__pycache__" -delete
```

## 🐛 Solución de Problemas

### Error de Conexión a Base de Datos
1. Verificar que MySQL esté corriendo
2. Confirmar credenciales en `.env`
3. Verificar que la base de datos existe

### Error de Módulos
```bash
pip install -r requirements.txt
```

### Error de Permisos
```bash
# En Windows, ejecutar como Administrador
# En Linux/Mac, usar sudo si es necesario
```

## � Despliegue y Distribución

### 🚀 **Instalación Rápida (3 Pasos)**

Para un despliegue rápido en otra máquina, consulta:
- **`docs/despliegue/INSTALACION-RAPIDA.txt`** - Guía de 3 pasos
- **`docs/despliegue/README.md`** - Índice completo de despliegue

### 📋 **Documentación de Despliegue Completa**

La carpeta `docs/despliegue/` contiene:

- **`INSTRUCCIONES-DEPLOY.md`** - Guía completa de despliegue
- **`.env.deploy-template`** - Plantilla de configuración 
- **`export-db.bat`** - Script para exportar base de datos
- **`INSTALACION-RAPIDA.txt`** - Guía express de instalación

### 📦 **Preparar Paquete de Despliegue**

1. **Exportar base de datos:**
   ```bash
   docs/despliegue/export-db.bat
   ```

2. **Archivos esenciales a incluir:**
   - Carpeta completa del proyecto
   - Base de datos exportada (dbflash.sql)
   - Archivo `.env` configurado
   - Documentación de `docs/despliegue/`

3. **En máquina destino:**
   - Descomprimir proyecto
   - Seguir `docs/despliegue/INSTALACION-RAPIDA.txt`
   - Ejecutar `install.bat`

## �📄 Documentación Adicional

- 📁 **`docs/ESTRUCTURA_PROYECTO.md`** - Estructura detallada
- 📁 **`docs/reportes/`** - Reportes de desarrollo (solo local)

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama para nueva feature: `git checkout -b feature/nueva-feature`
3. Commit de cambios: `git commit -m 'Agregar nueva feature'`
4. Push a la rama: `git push origin feature/nueva-feature`
5. Crear Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**Desarrollado con ❤️ por el equipo DomiFlash**  
*Última actualización: Octubre 2025*