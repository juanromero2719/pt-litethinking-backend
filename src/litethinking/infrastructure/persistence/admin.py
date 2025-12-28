from django.contrib import admin

from .empresa.model import EmpresaModel
from .producto.model import ProductoModel, ProductoPrecioModel


@admin.register(EmpresaModel)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre', 'direccion', 'telefono')
    search_fields = ('nit', 'nombre')
    list_filter = ('nombre',)


@admin.register(ProductoModel)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'empresa', 'caracteristicas')
    search_fields = ('codigo', 'nombre')
    list_filter = ('empresa',)
    raw_id_fields = ('empresa',)


@admin.register(ProductoPrecioModel)
class ProductoPrecioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'moneda', 'valor')
    list_filter = ('moneda',)
    search_fields = ('producto__codigo', 'producto__nombre')

