from rest_framework import serializers

from ....domain.entities.empresa import Empresa


class EmpresaSerializer(serializers.Serializer):

    nit = serializers.CharField(max_length=20, required=True, allow_blank=False)
    nombre = serializers.CharField(max_length=255, required=True, allow_blank=False)
    direccion = serializers.CharField(max_length=255, required=True, allow_blank=False)
    telefono = serializers.CharField(max_length=30, required=True, allow_blank=False)
    
    def to_representation(self, instance: Empresa):
        return {
            'nit': instance.nit,
            'nombre': instance.nombre,
            'direccion': instance.direccion,
            'telefono': instance.telefono,
        }

