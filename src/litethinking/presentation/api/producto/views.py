from decimal import Decimal
import os

from django.conf import settings
from openai import OpenAI
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....application.use_cases.producto_use_cases import (
    AgregarPrecioProductoUseCase,
    CrearProductoUseCase,
    EliminarProductoUseCase,
    ListarProductosUseCase,
    ObtenerProductoUseCase,
)
from ....domain.entities.producto import Moneda
from ....infrastructure.persistence.empresa.repository_impl import DjangoEmpresaRepository
from ....infrastructure.persistence.producto.repository_impl import DjangoProductoRepository
from ..permissions import IsAdmin
from .serializer import ProductoSerializer

empresa_repository = DjangoEmpresaRepository()
producto_repository = DjangoProductoRepository()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def productos_list_create(request):
    if request.method == 'GET':
        empresa_nit = request.query_params.get('empresa_nit')
        use_case = ListarProductosUseCase(producto_repository)
        productos = use_case.ejecutar(empresa_nit=empresa_nit)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            use_case = CrearProductoUseCase(producto_repository, empresa_repository)
            producto = use_case.ejecutar(
                codigo=request.data.get('codigo'),
                nombre=request.data.get('nombre'),
                empresa_nit=request.data.get('empresa_nit'),
                caracteristicas=request.data.get('caracteristicas'),
            )
            serializer = ProductoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def producto_detail(request, codigo):
    if request.method == 'GET':
        use_case = ObtenerProductoUseCase(producto_repository)
        producto = use_case.ejecutar(codigo)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        use_case = EliminarProductoUseCase(producto_repository)
        eliminado = use_case.ejecutar(codigo)
        if not eliminado:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def producto_agregar_precio(request, codigo):
    try:
        use_case = AgregarPrecioProductoUseCase(producto_repository)
        moneda = Moneda(request.data.get('moneda'))
        valor = Decimal(str(request.data.get('valor')))
        producto = use_case.ejecutar(
            codigo_producto=codigo,
            moneda=moneda,
            valor=valor
        )
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def producto_generar_descripcion(request):

    try:
        nombre = request.data.get('nombre', '').strip()
        if not nombre:
            return Response(
                {'error': 'El nombre del producto es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        caracteristicas_actuales = request.data.get('caracteristicas_actuales', '').strip()
        categoria = request.data.get('categoria', '').strip()
        precio = request.data.get('precio', '').strip()
        moneda = request.data.get('moneda', 'COP').strip()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return Response(
                {'error': 'OPENAI_API_KEY no está configurada en las variables de entorno'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        client = OpenAI(api_key=api_key)
        
        prompt_parts = [
            "Eres un experto en marketing y redacción de descripciones de productos.",
            "Tu tarea es crear una descripción llamativa, atractiva y profesional para un producto.",
            "",
            f"Nombre del producto: {nombre}"
        ]
        
        if categoria:
            prompt_parts.append(f"Categoría: {categoria}")
        
        if caracteristicas_actuales:
            prompt_parts.append(f"Características técnicas actuales: {caracteristicas_actuales}")
        
        if precio:
            precio_formateado = f"{float(precio):,.0f}".replace(',', '.')
            prompt_parts.append(f"Precio: {precio_formateado} {moneda}")
        
        prompt_parts.extend([
            "",
            "Requisitos para la descripción:",
            "- Debe ser atractiva y persuasiva",
            "- Destacar los beneficios principales del producto",
            "- Usar un lenguaje profesional pero accesible",
            "- Máximo 200 palabras",
            "- En español",
            "- No incluir el nombre del producto en la descripción (solo describir)",
            "",
            "Genera únicamente la descripción, sin títulos ni encabezados:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en marketing y redacción de descripciones de productos. Generas descripciones atractivas, profesionales y persuasivas."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        descripcion = response.choices[0].message.content.strip()
        
        return Response(
            {
                'descripcion': descripcion,
                'nombre_producto': nombre,
                'modelo_usado': 'gpt-4o-mini'
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': f'Error al generar la descripción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

