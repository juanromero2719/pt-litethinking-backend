from django.db import models

from ..empresa.model import EmpresaModel

class ProductoModel(models.Model):

    codigo = models.CharField("Código", max_length=50, primary_key=True)
    nombre = models.CharField("Nombre del producto", max_length=255)
    caracteristicas = models.TextField("Características", blank=True)
    descripcion = models.TextField("Descripción", blank=True, null=True)

    empresa = models.ForeignKey(
        EmpresaModel,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    class Meta:
        db_table = "producto"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class ProductoPrecioModel(models.Model):

    class Moneda(models.TextChoices):
        COP = "COP", "Peso colombiano"
        USD = "USD", "Dólar"
        EUR = "EUR", "Euro"

    producto = models.ForeignKey(
        ProductoModel,
        on_delete=models.CASCADE,
        related_name="precios",
    )

    moneda = models.CharField("Moneda", max_length=3, choices=Moneda.choices)
    valor = models.DecimalField("Precio", max_digits=14, decimal_places=2)

    class Meta:
        db_table = "producto_precio"
        verbose_name = "Precio de Producto"
        verbose_name_plural = "Precios de Productos"
        constraints = [
            models.UniqueConstraint(
                fields=["producto", "moneda"],
                name="uq_producto_precio__producto_moneda",
            )
        ]

    def __str__(self):
        return f"{self.producto.codigo} {self.moneda} {self.valor}"

