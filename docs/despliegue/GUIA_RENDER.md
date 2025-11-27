# 🚀 Guía de Despliegue en Render - DomiFlash

## Paso 1: Crear Base de Datos PostgreSQL en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en **New +** → **PostgreSQL**
3. Configura:
   - **Name:** `domiflash-db`
   - **Database:** `dbflash`
   - **User:** `domiflash_user`
   - **Region:** Oregon (o la más cercana)
   - **Plan:** Free (90 días gratis)
4. Click **Create Database**
5. Espera que se cree y copia los datos de conexión:
   - **Internal Database URL** (para la app)
   - **External Database URL** (para importar datos)

## Paso 2: Importar la Base de Datos

### Opción A: Usando psql desde terminal
```bash
# Instalar PostgreSQL client si no lo tienes
# Windows: descargar de https://www.postgresql.org/download/

# Importar el SQL
psql "TU_EXTERNAL_DATABASE_URL" -f database/dbflash_postgresql.sql
```

### Opción B: Usando herramienta gráfica (DBeaver, pgAdmin)
1. Conectar usando External Database URL
2. Abrir archivo `database/dbflash_postgresql.sql`
3. Ejecutar todo el script

## Paso 3: Crear Web Service en Render

1. En Render, click **New +** → **Web Service**
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name:** `domiflash`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

## Paso 4: Variables de Entorno

En la sección **Environment** del Web Service, agrega:

```
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_USER=domiflash_user
DB_PASSWORD=tu_password_de_render
DB_NAME=dbflash
SECRET_KEY=genera_una_clave_secreta_larga
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
MAIL_DEFAULT_SENDER=tu_email@gmail.com
SESSION_COOKIE_SECURE=True
```

## Paso 5: Deploy

1. Click **Create Web Service**
2. Render automáticamente:
   - Clona tu repo
   - Instala dependencias
   - Inicia la aplicación
3. Tu app estará disponible en: `https://domiflash.onrender.com`

---

## 📋 Checklist Pre-Deploy

- [ ] Subir cambios a GitHub (ver comandos abajo)
- [ ] Crear PostgreSQL en Render
- [ ] Importar `dbflash_postgresql.sql`
- [ ] Crear Web Service
- [ ] Configurar variables de entorno
- [ ] Verificar que la app funciona

---

## 🔐 Notas de Seguridad

1. **Nunca** subas el archivo `.env` a GitHub
2. Genera una `SECRET_KEY` nueva para producción:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Para Gmail, usa una "Contraseña de Aplicación", no tu contraseña normal
