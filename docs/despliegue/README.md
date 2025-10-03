# 📦 DOCUMENTACIÓN DE DESPLIEGUE - DOMIFLASH

Esta carpeta contiene toda la documentación y herramientas necesarias para desplegar el proyecto DomiFlash en diferentes entornos.

## 📋 Contenido de la Carpeta

### 🚀 Guías de Instalación
- **`INSTALACION-RAPIDA.txt`** - Guía de 3 pasos para instalación rápida
- **`INSTRUCCIONES-DEPLOY.md`** - Documentación completa de despliegue

### ⚙️ Herramientas de Configuración  
- **`.env.deploy-template`** - Plantilla de archivo de configuración
- **`export-db.bat`** - Script para exportar base de datos MySQL

## 🎯 Flujo de Despliegue Recomendado

1. **Preparación Local:**
   ```bash
   # Ejecutar desde la raíz del proyecto
   docs/despliegue/export-db.bat
   ```

2. **Empaquetar para Transporte:**
   - Carpeta completa del proyecto
   - Base de datos exportada (dbflash.sql o dbflash_backup.sql)
   - Documentación de esta carpeta

3. **Instalación en Destino:**
   - Seguir `INSTALACION-RAPIDA.txt`
   - Usar `.env.deploy-template` como base
   - Importar base de datos
   - Ejecutar `install.bat`

## 📚 Documentación Adicional

Para documentación técnica completa del proyecto, consultar:
- `../ESTRUCTURA_PROYECTO.md`
- `../ORGANIZACION_PROYECTO.md`
- `../../README.md`

## 🆘 Soporte

Si encuentras problemas durante el despliegue:
1. Revisa `INSTALACION-RAPIDA.txt` 
2. Consulta `INSTRUCCIONES-DEPLOY.md`
3. Verifica los reportes en `../reportes/`