# Guía de Despliegue en Vercel

Este documento explica cómo desplegar el proyecto Django en Vercel.

## 📋 Requisitos Previos

1. Cuenta en Vercel (https://vercel.com)
2. Repositorio Git (GitHub, GitLab o Bitbucket)
3. Base de datos PostgreSQL (Supabase, Railway, o similar)

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de que tu código esté en un repositorio Git:

```bash
git add .
git commit -m "Preparado para Vercel"
git push
```

### 1.5. Generar SECRET_KEY (Opcional pero Recomendado)

Puedes generar una SECRET_KEY usando el script incluido:

```bash
# Con Poetry:
poetry run python generate_secret_key.py

# O directamente:
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Configurar Variables de Entorno en Vercel

En el dashboard de Vercel, ve a tu proyecto → Settings → Environment Variables y agrega:

```
SECRET_KEY=tu-secret-key-generado
DEBUG=False
ALLOWED_HOSTS=tu-proyecto.vercel.app,localhost
DB_NAME=nombre_de_tu_db
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=host_db
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,http://localhost:3000
```

**Importante:** 
- Genera un nuevo `SECRET_KEY` para producción:
  ```bash
  # Si usas Poetry (recomendado):
  poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  
  # Si usas Python directamente:
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  
  # O en Windows con py:
  py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Reemplaza `tu-proyecto.vercel.app` con tu dominio real de Vercel
- Reemplaza `tu-frontend.vercel.app` con el dominio de tu frontend

### 3. Importar Proyecto en Vercel

1. Ve a https://vercel.com/new
2. Selecciona tu repositorio
3. Vercel detectará automáticamente que es un proyecto Python
4. Configuración:
   - **Framework Preset:** Other
   - **Root Directory:** `LiteThinking` (si tu proyecto está en una subcarpeta)
   - **Build Command:** (dejar vacío)
   - **Output Directory:** (dejar vacío)
   - **Install Command:** `pip install -r requirements.txt`

### 4. Ejecutar Migraciones

Después del despliegue, necesitas ejecutar las migraciones. Puedes hacerlo de dos formas:

**Opción A: Usando Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel env pull .env.local
python manage.py migrate
```

**Opción B: Usando un script de build**
Crea un script que ejecute las migraciones automáticamente.

### 5. Verificar el Despliegue

Una vez desplegado, verifica que:
- ✅ La API responde en `https://tu-proyecto.vercel.app/api/auth/login/`
- ✅ Las variables de entorno están configuradas correctamente
- ✅ La conexión a la base de datos funciona

## 🔧 Archivos Creados para Vercel

- `vercel.json`: Configuración de rutas y builds
- `api/index.py`: Handler serverless para Django
- `requirements.txt`: Dependencias Python
- `.vercelignore`: Archivos a excluir del despliegue

## ⚠️ Limitaciones de Vercel con Django

1. **Cold Starts**: Las funciones serverless pueden tener un tiempo de inicio frío
2. **Tiempo de ejecución**: Máximo 10 segundos en plan gratuito, 60 segundos en Pro
3. **Base de datos**: Necesitas una base de datos externa (no SQLite)
4. **Archivos estáticos**: Considera usar un CDN para archivos estáticos grandes

## 🐛 Solución de Problemas

### Error: "TypeError: issubclass() arg 1 must be a class"
Este error indica que Vercel no está reconociendo correctamente el handler. Soluciones:

1. **Verifica que `api/index.py` exporte `app` directamente:**
   ```python
   from config.wsgi import application
   app = application
   ```

2. **Asegúrate de que `vercel.json` esté en la raíz del proyecto Django**

3. **Verifica que el `Root Directory` en Vercel apunte a `LiteThinking`** (si tu proyecto está en una subcarpeta)

4. **Si el error persiste**, intenta usar el formato alternativo en `api/index.py`:
   ```python
   # Exportar directamente sin wrapper
   app = application
   ```

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Asegúrate de que el `Root Directory` en Vercel apunte a la carpeta correcta

### Error: "Database connection failed"
- Verifica las variables de entorno de la base de datos
- Asegúrate de que tu base de datos permita conexiones desde Vercel (whitelist IPs)

### Error: "CORS"
- Verifica que `CORS_ALLOWED_ORIGINS` incluya tu dominio de frontend
- Asegúrate de que `CORS_ALLOW_CREDENTIALS = True`

## 📚 Recursos

- [Documentación de Vercel Python](https://vercel.com/docs/frameworks/python)
- [Django en Vercel](https://vercel.com/guides/deploying-django-with-vercel)

