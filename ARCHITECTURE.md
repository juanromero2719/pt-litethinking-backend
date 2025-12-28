# Arquitectura Limpia - LiteThinking

Este proyecto implementa **Arquitectura Limpia (Clean Architecture)** siguiendo los principios de separación de responsabilidades y desacoplamiento de capas.

## 📁 Estructura del Proyecto

```
LiteThinking/
├── src/
│   └── litethinking/
│       ├── domain/                    # 🟢 CAPA DE DOMINIO (Núcleo)
│       │   ├── entities/              # Entidades del negocio (sin Django)
│       │   │   ├── empresa.py
│       │   │   └── producto.py
│       │   └── ports/                 # Interfaces (contratos)
│       │       ├── empresa_repository.py
│       │       └── producto_repository.py
│       │
│       ├── application/               # 🟡 CAPA DE APLICACIÓN
│       │   └── use_cases/             # Casos de uso
│       │       ├── empresa_use_cases.py
│       │       └── producto_use_cases.py
│       │
│       ├── infrastructure/            # 🔵 CAPA DE INFRAESTRUCTURA
│       │   └── persistence/          # Implementaciones concretas
│       │       ├── django_models.py  # Modelos de Django
│       │       ├── empresa_repository_impl.py
│       │       └── producto_repository_impl.py
│       │
│       └── presentation/              # 🟠 CAPA DE PRESENTACIÓN
│           └── api/                   # APIs REST
│               ├── views.py
│               └── serializers.py
│
├── config/                            # Configuración de Django
├── empresas/                          # App legacy (mantener por migraciones)
└── productos/                         # App legacy (mantener por migraciones)
```

## 🎯 Principios de Arquitectura Limpia

### 1. **Capa de Dominio** (Núcleo)
- ✅ **Sin dependencias externas**: No depende de Django, frameworks o bases de datos
- ✅ **Entidades puras**: Representan los conceptos del negocio
- ✅ **Reglas de negocio**: Validaciones y lógica de dominio
- ✅ **Puertos (Interfaces)**: Define contratos que deben cumplir las implementaciones

**Ejemplo:**
```python
# domain/entities/empresa.py
class Empresa:
    def __init__(self, nit: str, nombre: str, ...):
        self._validar_nit(nit)  # Regla de negocio
        self.nit = nit
        # ...
```

### 2. **Capa de Aplicación**
- ✅ **Casos de uso**: Orquestan las operaciones del negocio
- ✅ **Depende solo del dominio**: Usa las entidades y puertos del dominio
- ✅ **Lógica de aplicación**: Coordina entre repositorios y entidades

**Ejemplo:**
```python
# application/use_cases/empresa_use_cases.py
class CrearEmpresaUseCase:
    def ejecutar(self, nit: str, nombre: str, ...):
        if self._empresa_repository.existe(nit):
            raise ValueError("Empresa ya existe")
        empresa = Empresa(nit, nombre, ...)
        return self._empresa_repository.guardar(empresa)
```

### 3. **Capa de Infraestructura**
- ✅ **Implementaciones concretas**: Implementa los puertos del dominio
- ✅ **Depende del dominio y aplicación**: Usa Django ORM para persistir
- ✅ **Modelos de Django**: Mapean entre entidades de dominio y base de datos

**Ejemplo:**
```python
# infrastructure/persistence/empresa_repository_impl.py
class DjangoEmpresaRepository(EmpresaRepository):
    def guardar(self, empresa: Empresa) -> Empresa:
        empresa_model = EmpresaModel.objects.update_or_create(...)
        return self._to_domain_entity(empresa_model)
```

### 4. **Capa de Presentación**
- ✅ **APIs REST**: Expone la funcionalidad mediante HTTP
- ✅ **Serializers**: Convierte entre entidades y DTOs
- ✅ **Depende de aplicación**: Usa casos de uso para ejecutar operaciones

**Ejemplo:**
```python
# presentation/api/views.py
@api_view(['POST'])
def empresas_list_create(request):
    use_case = CrearEmpresaUseCase(empresa_repository)
    empresa = use_case.ejecutar(...)
    return Response(EmpresaSerializer(empresa).data)
```

## 🔄 Flujo de Datos

```
Cliente HTTP
    ↓
[Presentación] API Views
    ↓
[Aplicación] Use Cases
    ↓
[Dominio] Entities + Ports (Interfaces)
    ↓
[Infraestructura] Repository Implementations
    ↓
Django ORM → Base de Datos
```

## ✅ Ventajas de esta Arquitectura

1. **Desacoplamiento**: El dominio no depende de frameworks
2. **Testabilidad**: Fácil de testear cada capa independientemente
3. **Mantenibilidad**: Cambios en una capa no afectan otras
4. **Flexibilidad**: Puedes cambiar Django por otro framework sin tocar el dominio
5. **Claridad**: Separación clara de responsabilidades

## 📝 Uso de las APIs

### Empresas

```bash
# Crear empresa
POST /api/empresas/
{
  "nit": "123456789",
  "nombre": "Mi Empresa",
  "direccion": "Calle 123",
  "telefono": "3001234567"
}

# Listar empresas
GET /api/empresas/

# Obtener empresa
GET /api/empresas/{nit}/

# Actualizar empresa
PUT /api/empresas/{nit}/

# Eliminar empresa
DELETE /api/empresas/{nit}/
```

### Productos

```bash
# Crear producto
POST /api/productos/
{
  "codigo": "PROD001",
  "nombre": "Producto 1",
  "empresa_nit": "123456789",
  "caracteristicas": "Descripción"
}

# Listar productos
GET /api/productos/
GET /api/productos/?empresa_nit=123456789

# Agregar precio
POST /api/productos/{codigo}/precios/
{
  "moneda": "COP",
  "valor": "100000.00"
}
```

## 🔧 Configuración

El proyecto está configurado para usar las nuevas capas mientras mantiene compatibilidad con las apps legacy (`empresas` y `productos`) para las migraciones existentes.

Las nuevas entidades y lógica de negocio están en `src/litethinking/`, completamente desacopladas de Django.

