# LiteThinking Backend

Proyecto desplegado en: https://pt-litethinking-backend.vercel.app

API REST desarrollada con Django y Django REST Framework, implementando **Clean Architecture** para gestionar empresas y productos con autenticación JWT y control de acceso basado en roles.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Arquitectura](#arquitectura)
- [Endpoints](#endpoints)
- [Autenticación y Roles](#autenticación-y-roles)
- [Estructura del Proyecto](#estructura-del-proyecto)

## 🔧 Requisitos Previos

- Python 3.12 o superior
- Poetry (gestor de dependencias)
- PostgreSQL (base de datos)
- Git

### Instalar Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/Mac
curl -sSL https://install.python-poetry.org | python3 -
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd LiteThinking/LiteThinking
```

### 2. Instalar dependencias

```bash
poetry install
```

### 3. Activar el entorno virtual

```bash
poetry shell
```

### 4. Crear archivo de variables de entorno

Crea un archivo `.env` en la raíz del proyecto (`LiteThinking/`) con las siguientes variables:

```env
# Base de datos
DB_NAME=litethinking
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=tu-secret-key-generada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Email (opcional, para envío de PDFs)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=tu-email@gmail.com

# OpenAI (opcional, para generación de descripciones)
OPENAI_API_KEY=sk-proj-tu-api-key
```

### 5. Generar SECRET_KEY (opcional)

Si no tienes una SECRET_KEY, puedes generarla:

```bash
poetry run python generate_secret_key.py
```

### 6. Crear la base de datos PostgreSQL

```sql
CREATE DATABASE litethinking;
```

### 7. Ejecutar migraciones

```bash
poetry run python manage.py migrate
```

### 8. Crear grupos de roles

```bash
poetry run python manage.py crear_grupos
```

### 9. Crear superusuario (opcional)

```bash
poetry run python manage.py createsuperuser
```

## ⚙️ Configuración

### Variables de Entorno Importantes

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `DB_NAME` | Nombre de la base de datos PostgreSQL | ✅ |
| `DB_USER` | Usuario de PostgreSQL | ✅ |
| `DB_PASSWORD` | Contraseña de PostgreSQL | ✅ |
| `DB_HOST` | Host de PostgreSQL | ✅ |
| `DB_PORT` | Puerto de PostgreSQL | ✅ |
| `SECRET_KEY` | Clave secreta de Django | ✅ |
| `DEBUG` | Modo debug (True/False) | ✅ |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS | ✅ |
| `OPENAI_API_KEY` | API Key de OpenAI | ⚠️ (solo para generación de descripciones) |
| `EMAIL_HOST_USER` | Usuario SMTP | ⚠️ (solo para envío de emails) |
| `EMAIL_HOST_PASSWORD` | Contraseña SMTP | ⚠️ (solo para envío de emails) |

## ▶️ Ejecución

### Modo Desarrollo

```bash
poetry run python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

### Recolectar archivos estáticos

```bash
poetry run python manage.py collectstatic
```

### Ejecutar tests (si existen)

```bash
poetry run python manage.py test
```

## 🏗️ Arquitectura

Este proyecto implementa **Clean Architecture** (Arquitectura Limpia), separando el código en capas independientes:

### Capas de la Arquitectura

```
┌─────────────────────────────────────────┐
│     PRESENTATION (API/REST)            │  ← Capa más externa
│  - Views, Serializers, URLs             │
├─────────────────────────────────────────┤
│     APPLICATION (Use Cases)             │
│  - Casos de uso del negocio             │
├─────────────────────────────────────────┤
│     DOMAIN (Entidades y Puertos)         │  ← Núcleo del negocio
│  - Entities, Value Objects, Ports      │
├─────────────────────────────────────────┤
│     INFRASTRUCTURE (Implementaciones)   │
│  - Django Models, Repositories          │
└─────────────────────────────────────────┘
```

### Principios

1. **Independencia de Frameworks**: El dominio no depende de Django
2. **Testabilidad**: Cada capa puede probarse independientemente
3. **Independencia de UI**: La lógica de negocio no depende de la API
4. **Independencia de Base de Datos**: El dominio no conoce la BD
5. **Inversión de Dependencias**: Las capas externas dependen de las internas

### Flujo de Datos

```
Request → View → Use Case → Repository → Database
                ↓
         Domain Entity
                ↓
Response ← Serializer ← Use Case ← Repository
```

## 📡 Endpoints

### Autenticación

#### Registro de Usuario
```http
POST /api/auth/registro/
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "contraseña123",
  "password_confirm": "contraseña123",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

**Respuesta:**
```json
{
  "message": "Usuario registrado exitosamente",
  "username": "usuario",
  "email": "usuario@example.com",
  "rol": "Externo"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json
Authorization: Bearer <refresh_token>

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Empresas

#### Listar Empresas
```http
GET /api/empresas/
Authorization: Bearer <access_token>
```

**Respuesta:**
```json
[
  {
    "nit": "900123456",
    "nombre": "Empresa Ejemplo",
    "direccion": "Calle 123",
    "telefono": "3001234567"
  }
]
```

#### Crear Empresa
```http
POST /api/empresas/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nit": "900123456",
  "nombre": "Empresa Ejemplo",
  "direccion": "Calle 123",
  "telefono": "3001234567"
}
```

#### Obtener Empresa
```http
GET /api/empresas/900123456/
Authorization: Bearer <access_token>
```

#### Actualizar Empresa
```http
PUT /api/empresas/900123456/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Empresa Actualizada",
  "direccion": "Nueva Dirección",
  "telefono": "3007654321"
}
```

#### Eliminar Empresa
```http
DELETE /api/empresas/900123456/
Authorization: Bearer <access_token>
```

**Nota:** No se puede eliminar una empresa que tenga productos asociados.

#### Listar Productos por Empresa
```http
GET /api/empresas/900123456/productos/
Authorization: Bearer <access_token>
```

### Productos

#### Listar Productos
```http
GET /api/productos/
Authorization: Bearer <access_token>
```

**Query Params opcionales:**
- `empresa_nit`: Filtrar productos por empresa

#### Crear Producto
```http
POST /api/productos/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "codigo": "PROD-001",
  "nombre": "Producto Ejemplo",
  "empresa_nit": "900123456",
  "caracteristicas": "Características técnicas",
  "descripcion": "Descripción opcional del producto"
}
```

#### Obtener Producto
```http
GET /api/productos/PROD-001/
Authorization: Bearer <access_token>
```

**Respuesta:**
```json
{
  "codigo": "PROD-001",
  "nombre": "Producto Ejemplo",
  "empresa_nit": "900123456",
  "caracteristicas": "Características técnicas",
  "descripcion": "Descripción del producto",
  "precios": [
    {
      "moneda": "COP",
      "valor": "150000.00"
    }
  ]
}
```

#### Eliminar Producto
```http
DELETE /api/productos/PROD-001/
Authorization: Bearer <access_token>
```

#### Agregar Precio a Producto
```http
POST /api/productos/PROD-001/precios/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "moneda": "COP",
  "valor": "150000.00"
}
```

**Monedas disponibles:** `COP`, `USD`, `EUR`

#### Generar Descripción con IA
```http
POST /api/productos/generar-descripcion/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Laptop HP",
  "caracteristicas_actuales": "Procesador Intel i7, 16GB RAM",
  "categoria": "Tecnología",
  "precio": "1500000",
  "moneda": "COP"
}
```

**Respuesta:**
```json
{
  "descripcion": "Descripción generada por OpenAI...",
  "nombre_producto": "Laptop HP",
  "modelo_usado": "gpt-4o-mini"
}
```

### Inventario

#### Generar PDF de Inventario
```http
GET /api/inventario/empresa/900123456/pdf/
Authorization: Bearer <access_token>
```

**Query Params opcionales:**
- `email`: Enviar el PDF por correo electrónico

**Ejemplo con email:**
```http
GET /api/inventario/empresa/900123456/pdf/?email=destino@example.com
Authorization: Bearer <access_token>
```

**Respuesta (sin email):**
- Archivo PDF descargable

**Respuesta (con email):**
```json
{
  "message": "El archivo PDF se está enviando a destino@example.com",
  "empresa_nit": "900123456",
  "empresa_nombre": "Empresa Ejemplo",
  "email_destino": "destino@example.com",
  "total_productos": 10,
  "fecha_generacion": "29/12/2025 10:30:45"
}
```

## 🔐 Autenticación y Roles

### Sistema de Roles

El proyecto utiliza el sistema de grupos de Django para gestionar roles:

- **Admin**: Acceso completo a todos los endpoints
- **Externo**: Solo lectura de empresas

### Permisos por Endpoint

| Endpoint | Admin | Externo |
|----------|-------|---------|
| `POST /api/auth/registro/` | ✅ | ✅ |
| `POST /api/auth/login/` | ✅ | ✅ |
| `GET /api/empresas/` | ✅ | ✅ (solo lectura) |
| `POST /api/empresas/` | ✅ | ❌ |
| `PUT /api/empresas/<nit>/` | ✅ | ❌ |
| `DELETE /api/empresas/<nit>/` | ✅ | ❌ |
| `GET /api/productos/` | ✅ | ❌ |
| `POST /api/productos/` | ✅ | ❌ |
| `DELETE /api/productos/<codigo>/` | ✅ | ❌ |
| `POST /api/productos/<codigo>/precios/` | ✅ | ❌ |
| `POST /api/productos/generar-descripcion/` | ✅ | ❌ |
| `GET /api/inventario/empresa/<nit>/pdf/` | ✅ | ❌ |

### Asignar Rol Admin a un Usuario

```bash
poetry run python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='usuario')
admin_group = Group.objects.get(name='Admin')
user.groups.add(admin_group)
```

## 📁 Estructura del Proyecto

```
LiteThinking/
├── config/                    # Configuración de Django
│   ├── settings.py           # Configuración principal
│   ├── urls.py               # Rutas principales
│   └── wsgi.py               # WSGI para producción
│
├── src/
│   └── litethinking/
│       ├── domain/           # 🟢 CAPA DE DOMINIO
│       │   ├── entities/     # Entidades del negocio
│       │   │   ├── empresa.py
│       │   │   └── producto.py
│       │   └── ports/        # Interfaces (contratos)
│       │       ├── empresa_repository.py
│       │       └── producto_repository.py
│       │
│       ├── application/       # 🟡 CAPA DE APLICACIÓN
│       │   └── use_cases/    # Casos de uso
│       │       ├── empresa_use_cases.py
│       │       └── producto_use_cases.py
│       │
│       ├── infrastructure/    # 🔵 CAPA DE INFRAESTRUCTURA
│       │   └── persistence/  # Implementaciones
│       │       ├── empresa/
│       │       │   ├── model.py
│       │       │   └── repository_impl.py
│       │       ├── producto/
│       │       │   ├── model.py
│       │       │   └── repository_impl.py
│       │       └── migrations/
│       │
│       └── presentation/      # 🟠 CAPA DE PRESENTACIÓN
│           └── api/          # APIs REST
│               ├── auth/
│               │   ├── views.py
│               │   └── serializer.py
│               ├── empresa/
│               │   ├── views.py
│               │   └── serializer.py
│               ├── producto/
│               │   ├── views.py
│               │   └── serializer.py
│               ├── inventario/
│               │   └── views.py
│               └── permissions.py
│
├── manage.py
├── pyproject.toml            # Dependencias (Poetry)
├── requirements.txt           # Dependencias (pip)
├── .env                       # Variables de entorno (no versionado)
└── README.md                  # Este archivo
```

## 🛠️ Comandos Útiles

### Gestión de Base de Datos

```bash
# Crear migraciones
poetry run python manage.py makemigrations

# Aplicar migraciones
poetry run python manage.py migrate

# Ver estado de migraciones
poetry run python manage.py showmigrations
```

### Gestión de Usuarios

```bash
# Crear superusuario
poetry run python manage.py createsuperuser

# Crear grupos de roles
poetry run python manage.py crear_grupos
```

### Desarrollo

```bash
# Verificar configuración
poetry run python manage.py check

# Recolectar archivos estáticos
poetry run python manage.py collectstatic

# Abrir shell de Django
poetry run python manage.py shell
```

## 📝 Notas Importantes

1. **Trailing Slashes**: Los endpoints funcionan tanto con como sin barra final (`/api/empresas/` y `/api/empresas`)

2. **Autenticación JWT**: Todos los endpoints (excepto registro y login) requieren un token JWT en el header:
   ```
   Authorization: Bearer <access_token>
   ```

3. **Tokens JWT**: Los tokens tienen un tiempo de expiración. Usa el endpoint `/api/auth/refresh/` para obtener un nuevo `access_token` con el `refresh_token`.

4. **Eliminación de Empresas**: No se puede eliminar una empresa que tenga productos asociados. Primero elimina los productos.

5. **Generación de Descripciones**: Requiere configuración de `OPENAI_API_KEY` en las variables de entorno.

6. **Envío de Emails**: Requiere configuración de SMTP en las variables de entorno.

## 🚀 Despliegue

Este proyecto está configurado para desplegarse en **Vercel**. Ver `vercel.json` y `api/index.py` para más detalles.

## 📄 Licencia

Este proyecto es privado y de uso interno.

## 👥 Autor

Sebastian Hogar - juan.romero@eduxperia.com

