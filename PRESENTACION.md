# 🎯 DomiFlash - Comandos para Presentación

## 🚀 Instalación Rápida (En Vivo)

```bash
# 1. Clonar proyecto
git clone https://github.com/domiflash/domiweb.git
cd domiweb

# 2. Verificar rama con funcionalidades
git checkout flujos
git status

# 3. Instalación automática (Windows)
.\install.bat

# 4. Configurar .env (mostrar archivo de ejemplo)
copy .env.example .env
notepad .env

# 5. Iniciar aplicación
.\start.bat
```

## 🧪 URLs de Demostración

### 🔗 Principales
- **Página principal**: http://127.0.0.1:5000/
- **Login**: http://127.0.0.1:5000/auth/login
- **Registro**: http://127.0.0.1:5000/auth/register

### 🛡️ Sistemas de Seguridad (requiere login)
- **Prueba timeout**: http://127.0.0.1:5000/config/test-session-timeout
- **Prueba validaciones**: http://127.0.0.1:5000/config/test-validation
- **Actualizar perfil**: http://127.0.0.1:5000/config/update-profile

## 🔐 Usuarios de Prueba

### Admin
- **Email**: admin@domiflash
- **Contraseña**: 123456

### Cliente Demo
- **Email**: cliente@test.com
- **Contraseña**: 123

## 🎯 Puntos Clave para Demostrar

### 1. 🔐 Seguridad Avanzada (5 min)
```bash
# Login con validaciones flexibles
admin@domiflash / 123456

# Mostrar timeout de sesión
- Indicador visual (esquina inferior izquierda)
- Sistema de alertas automáticas
- Modal de extensión de sesión

# Recuperación de contraseña
- Email automático con token seguro
- Cambio de contraseña con validaciones
```

### 2. 🛡️ Validaciones Automáticas (3 min)
```bash
# URL: /config/test-validation
- Sanitización XSS automática
- Validación de emails flexible
- Fortaleza de contraseñas
- Caracteres seguros solamente
```

### 3. 🕐 Gestión de Sesiones (3 min)
```bash
# URL: /config/test-session-timeout
- Monitoreo en tiempo real
- Renovación automática en actividad
- Heartbeat cada 5 minutos
- Logout automático por inactividad
```

### 4. 📧 Sistema de Email (2 min)
```bash
# Recuperación de contraseña
- Flask-Mail + Gmail SMTP
- Templates HTML profesionales
- Tokens seguros con expiración
- Confirmación de cambio
```

### 5. 💼 Funcionalidades de Negocio (7 min)
```bash
# Dashboard multirol
- Cliente: Carrito, pedidos, perfil
- Restaurante: Productos, pedidos, gestión
- Admin: Usuarios, estadísticas, configuración

# Progressive Web App
- Instalable en móvil/desktop
- Funciona offline
- Dark mode persistente
```

## 🔧 Comandos de Troubleshooting

### Verificar Estado
```bash
# Verificar conexión BD
python -c "from app import create_app; app = create_app(); print('BD OK' if app.db else 'BD Error')"

# Verificar dependencias
pip check

# Ver logs en tiempo real
python app.py | findstr "ERROR|WARNING"
```

### Reset Rápido
```bash
# Limpiar sesiones
rmdir /s flask_session
mkdir flask_session

# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Reset git (si es necesario)
git reset --hard HEAD
git clean -fd
```

## 📊 Métricas de Código

```bash
# Contar líneas de código
find . -name "*.py" | xargs wc -l

# Estructura del proyecto
tree /f | findstr /v "__pycache__"

# Commits y cambios
git log --oneline -10
git diff --stat
```

## 🎯 Agenda de Presentación (30 min)

### 📋 Introducción (5 min)
1. **Problema**: Sistemas de delivery inseguros
2. **Solución**: DomiFlash con seguridad robusta
3. **Tecnologías**: Flask, MySQL, TailwindCSS, PWA

### 🔧 Instalación en Vivo (5 min)
1. **Clonar**: git clone + checkout flujos
2. **Instalar**: ./install.bat
3. **Configurar**: .env con BD y email
4. **Ejecutar**: ./start.bat

### 🛡️ Seguridad Implementada (10 min)
1. **Login flexible**: admin@domiflash
2. **Timeout inteligente**: /config/test-session-timeout
3. **Validaciones**: /config/test-validation
4. **Email recovery**: Demostración completa

### 💼 Funcionalidades (8 min)
1. **Dashboard multirol**: Admin, cliente, restaurante
2. **Carrito de compras**: AJAX dinámico
3. **PWA**: Instalación móvil
4. **Dark mode**: Persistente

### 🎯 Conclusión (2 min)
1. **Logros**: Sistema completo y seguro
2. **Tecnología**: Moderna y escalable
3. **Código**: Limpio y documentado

## 📝 Notas para el Presentador

### ✅ Preparación Previa
- [ ] Verificar que MySQL está corriendo
- [ ] Configurar .env con datos reales
- [ ] Probar login con admin@domiflash
- [ ] Verificar que llegan emails
- [ ] Tener datos de prueba listos

### 🎯 Puntos Clave a Mencionar
- **Seguridad desde el diseño** (no agregada después)
- **Código limpio y modular** (fácil mantenimiento)
- **Tecnologías modernas** (PWA, AJAX, responsive)
- **Sistema robusto** (reconexión automática BD)
- **Experiencia de usuario** (dark mode, timeout inteligente)

### 🚨 Posibles Preguntas
1. **¿Por qué Flask?** → Rapidez, flexibilidad, Python
2. **¿Escalabilidad?** → Modular, fácil agregar funciones
3. **¿Seguridad?** → Timeout, validaciones, sanitización
4. **¿Mobile?** → PWA instalable, responsive design
5. **¿Producción?** → Waitress, HTTPS, variables seguras