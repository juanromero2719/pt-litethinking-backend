from decimal import Decimal
from typing import List, Optional

from ...domain.entities.producto import Moneda, Producto, ProductoPrecio
from ...domain.ports.empresa_repository import EmpresaRepository
from ...domain.ports.producto_repository import ProductoRepository


class CrearProductoUseCase:
    
    def __init__(
        self,
        producto_repository: ProductoRepository,
        empresa_repository: EmpresaRepository
    ):
        self._producto_repository = producto_repository
        self._empresa_repository = empresa_repository
    
    def ejecutar(
        self,
        codigo: str,
        nombre: str,
        empresa_nit: str,
        caracteristicas: Optional[str] = None
    ) -> Producto:
       
        if self._producto_repository.existe(codigo):
            raise ValueError(f"Ya existe un producto con el código: {codigo}")
        
        if not self._empresa_repository.existe(empresa_nit):
            raise ValueError(f"No existe una empresa con el NIT: {empresa_nit}")
        
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            empresa_nit=empresa_nit,
            caracteristicas=caracteristicas
        )
        
        return self._producto_repository.guardar(producto)


class ObtenerProductoUseCase:
    
    def __init__(self, producto_repository: ProductoRepository):
        self._producto_repository = producto_repository
    
    def ejecutar(self, codigo: str) -> Optional[Producto]:
        return self._producto_repository.buscar_por_codigo(codigo)


class ListarProductosUseCase:
    
    def __init__(self, producto_repository: ProductoRepository):
        self._producto_repository = producto_repository
    
    def ejecutar(self, empresa_nit: Optional[str] = None) -> List[Producto]:

        if empresa_nit:
            return self._producto_repository.listar_por_empresa(empresa_nit)
        return self._producto_repository.listar_todos()


class AgregarPrecioProductoUseCase:
    
    def __init__(self, producto_repository: ProductoRepository):
        self._producto_repository = producto_repository
    
    def ejecutar(
        self,
        codigo_producto: str,
        moneda: Moneda,
        valor: Decimal
    ) -> Producto:

        producto = self._producto_repository.buscar_por_codigo(codigo_producto)
        if not producto:
            raise ValueError(f"No existe un producto con el código: {codigo_producto}")
        
        precio = ProductoPrecio(moneda=moneda, valor=valor)
        producto.agregar_precio(precio)
        
        return self._producto_repository.guardar(producto)


class EliminarProductoUseCase:
    
    def __init__(self, producto_repository: ProductoRepository):
        self._producto_repository = producto_repository
    
    def ejecutar(self, codigo: str) -> bool:
        return self._producto_repository.eliminar(codigo)

