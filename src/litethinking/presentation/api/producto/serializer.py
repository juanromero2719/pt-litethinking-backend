from rest_framework import serializers

from ....domain.entities.producto import Moneda, Producto, ProductoPrecio


class ProductoPrecioSerializer(serializers.Serializer):
    moneda = serializers.ChoiceField(choices=[m.value for m in Moneda])
    valor = serializers.DecimalField(max_digits=14, decimal_places=2)
    
    def to_representation(self, instance: ProductoPrecio):
        return {
            'moneda': instance.moneda.value,
            'valor': str(instance.valor),
        }


class ProductoSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=255)
    empresa_nit = serializers.CharField(max_length=20)
    caracteristicas = serializers.CharField(allow_blank=True, required=False)
    descripcion = serializers.CharField(allow_blank=True, required=False)
    precios = ProductoPrecioSerializer(many=True, required=False)
    
    def to_representation(self, instance: Producto):
        return {
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'empresa_nit': instance.empresa_nit,
            'caracteristicas': instance.caracteristicas,
            'descripcion': instance.descripcion,
            'precios': [
                ProductoPrecioSerializer().to_representation(precio)
                for precio in instance.precios
            ],
        }

