"""
Módulo de presentación API para Producto
"""
from .serializer import ProductoPrecioSerializer, ProductoSerializer
from .views import (
    producto_agregar_precio,
    producto_detail,
    producto_generar_descripcion,
    productos_list_create,
)

__all__ = [
    'ProductoSerializer', 
    'ProductoPrecioSerializer',
    'producto_agregar_precio',
    'producto_detail',
    'producto_generar_descripcion',
    'productos_list_create',
]

