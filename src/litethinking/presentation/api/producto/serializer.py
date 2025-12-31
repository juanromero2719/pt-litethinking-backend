import re
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
    
    def validate_codigo(self, value):
        """Valida que el código siga el formato nombre-numero"""
        if not value or not value.strip():
            raise serializers.ValidationError("El código del producto es requerido")
        
        codigo_pattern = re.compile(r'^[A-Za-z]+-\d+$')
        if not codigo_pattern.match(value.strip()):
            raise serializers.ValidationError(
                "El código debe seguir el formato 'nombre-numero' (ej: PROD-001, LAPTOP-123). "
                "Solo se permiten letras, un guion y números."
            )
        
        return value.strip()
    
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

