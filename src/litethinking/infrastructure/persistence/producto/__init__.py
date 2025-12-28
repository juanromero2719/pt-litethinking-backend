"""
Módulo de persistencia para Producto
"""
from .model import ProductoModel, ProductoPrecioModel
from .repository_impl import DjangoProductoRepository

__all__ = ['ProductoModel', 'ProductoPrecioModel', 'DjangoProductoRepository']

