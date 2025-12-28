from typing import List, Optional

from ....domain.entities.producto import Moneda, Producto, ProductoPrecio
from ....domain.ports.producto_repository import ProductoRepository
from .model import ProductoModel, ProductoPrecioModel


class DjangoProductoRepository(ProductoRepository):

    def guardar(self, producto: Producto) -> Producto:
        producto_model, _ = ProductoModel.objects.update_or_create(
            codigo=producto.codigo,
            defaults={
                'nombre': producto.nombre,
                'caracteristicas': producto.caracteristicas,
                'empresa_id': producto.empresa_nit,
            }
        )
        
        ProductoPrecioModel.objects.filter(producto=producto_model).delete()
        for precio in producto.precios:
            ProductoPrecioModel.objects.create(
                producto=producto_model,
                moneda=precio.moneda.value,
                valor=precio.valor
            )
        
        return self._to_domain_entity(producto_model)
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Producto]:
        try:
            producto_model = ProductoModel.objects.prefetch_related('precios').get(codigo=codigo)
            return self._to_domain_entity(producto_model)
        except ProductoModel.DoesNotExist:
            return None
    
    def listar_todos(self) -> List[Producto]:
        productos_model = ProductoModel.objects.prefetch_related('precios').all()
        return [self._to_domain_entity(prod) for prod in productos_model]
    
    def listar_por_empresa(self, empresa_nit: str) -> List[Producto]:
        productos_model = ProductoModel.objects.prefetch_related('precios').filter(
            empresa_id=empresa_nit
        )
        return [self._to_domain_entity(prod) for prod in productos_model]
    
    def eliminar(self, codigo: str) -> bool:
        try:
            producto_model = ProductoModel.objects.get(codigo=codigo)
            producto_model.delete()
            return True
        except ProductoModel.DoesNotExist:
            return False
    
    def existe(self, codigo: str) -> bool:
        return ProductoModel.objects.filter(codigo=codigo).exists()
    
    def _to_domain_entity(self, producto_model: ProductoModel) -> Producto:
        precios = []
        for precio_model in producto_model.precios.all():
            moneda = Moneda(precio_model.moneda)
            precio = ProductoPrecio(moneda=moneda, valor=precio_model.valor)
            precios.append(precio)
        
        return Producto(
            codigo=producto_model.codigo,
            nombre=producto_model.nombre,
            empresa_nit=producto_model.empresa_id,
            caracteristicas=producto_model.caracteristicas,
            precios=precios
        )

