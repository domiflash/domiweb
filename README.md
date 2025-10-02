# 🍕 DomiFlash - Sistema de Delivery

**Sistema web completo de gestión de pedidos y delivery** desarrollado con Flask, MySQL y TailwindCSS.

## ✨ Características Principales

- 🔐 **Sistema de autenticación** multirol (Admin, Cliente, Restaurante, Repartidor)
- 🛒 **Carrito de compras** dinámico con AJAX
- 💳 **Múltiples métodos de pago** (Efectivo, Tarjeta, Nequi, Daviplata)
- 📱 **Progressive Web App (PWA)** - Instalable en móviles
- 🌙 **Dark Mode** completo y persistente
- 📄 **Generación de facturas PDF**
- 🚚 **Gestión de repartidores** y tracking de pedidos
- 📊 **Dashboard administrativo** con estadísticas

## 🏗️ Estructura del Proyecto

```
domiweb/
├── 📁 models/          # Modelos de datos (Usuario, Pedido, Producto, etc.)
├── 📁 routes/          # Controladores por rol (admin, cliente, restaurante)
├── 📁 templates/       # Plantillas HTML organizadas por módulo
├── 📁 static/          # CSS, JS, imágenes y PWA assets
├── 📁 utils/           # Utilidades (auth, cálculos, helpers)
├── 📁 docs/            # Documentación del proyecto
├── 📁 scripts/         # Scripts SQL y utilidades
└── 📁 temp/            # Archivos temporales (no en Git)
```

## 🚀 Instalación Rápida

### 1. **Clonar y Preparar**
```bash
git clone https://github.com/domiflash/domiweb.git
cd domiweb
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 3. **Configurar Base de Datos**
Crear archivo `.env` en la raíz:

```env
DB_HOST=localhost
DB_USER=tu_usuario
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

## 📄 Documentación Adicional

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