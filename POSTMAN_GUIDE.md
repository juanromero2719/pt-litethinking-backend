# Guía de Uso de Postman con la API

## 🔐 Endpoint de Login

### Configuración Correcta

**⚠️ IMPORTANTE:** El endpoint solo acepta peticiones **POST**, no GET.

### 1. Método y URL

- **Método:** `POST` (no GET)
- **URL:** 
  - Producción: `https://pt-litethinking-backend.vercel.app/api/auth/login/`
  - Local: `http://localhost:8000/api/auth/login/`
  - ⚠️ **IMPORTANTE:** La URL **DEBE** terminar con `/` (trailing slash)
  - Si no incluyes el `/` al final, Django redirigirá y convertirá tu POST en GET, causando el error "Method GET not allowed"

### 2. Headers

```
Content-Type: application/json
```

### 3. Body (raw JSON)

Selecciona:
- **Body** → **raw** → **JSON**

```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

### 4. Respuesta Exitosa (200 OK)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 5. Errores Comunes

#### Error 405: "Method GET not allowed"
**Causa:** Estás usando GET en lugar de POST
**Solución:** Cambia el método a POST en Postman

#### Error 400: "Invalid HTTP_HOST header"
**Causa:** El dominio no está en ALLOWED_HOSTS
**Solución:** Agrega el dominio en las variables de entorno de Vercel:
```
ALLOWED_HOSTS=pt-litethinking-backend.vercel.app,*.vercel.app
```

#### Error 401: "No active account found"
**Causa:** Credenciales incorrectas
**Solución:** Verifica que el usuario y contraseña sean correctos

## 🔄 Endpoint de Refresh Token

### Configuración

- **Método:** `POST`
- **URL:** `https://pt-litethinking-backend.vercel.app/api/auth/refresh/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
    "refresh": "tu_refresh_token_aqui"
  }
  ```

### Respuesta Exitosa

```json
{
  "access": "nuevo_access_token"
}
```

## 🔒 Usar el Token en Peticiones Autenticadas

Después de obtener el `access` token, úsalo en el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Ejemplo en Postman

1. Ve a la pestaña **Authorization**
2. Selecciona **Type:** `Bearer Token`
3. Pega tu token en el campo **Token**

O manualmente en **Headers:**
```
Authorization: Bearer tu_token_aqui
```

## 📝 Colección de Postman Recomendada

Crea una colección con estas peticiones:

1. **Login**
   - POST `https://pt-litethinking-backend.vercel.app/api/auth/login/`
   - Body: `{"username": "admin", "password": "password"}`

2. **Refresh Token**
   - POST `https://pt-litethinking-backend.vercel.app/api/auth/refresh/`
   - Body: `{"refresh": "{{refresh_token}}"}`

3. **Petición Autenticada (ejemplo)**
   - GET/POST `https://pt-litethinking-backend.vercel.app/api/endpoint/`
   - Authorization: Bearer `{{access_token}}`

## ⚙️ Variables de Entorno en Postman

Crea variables de entorno en Postman para facilitar el uso:

- `base_url`: `https://pt-litethinking-backend.vercel.app`
- `access_token`: (se llena automáticamente después del login)
- `refresh_token`: (se llena automáticamente después del login)

Luego usa: `{{base_url}}/api/auth/login/`

