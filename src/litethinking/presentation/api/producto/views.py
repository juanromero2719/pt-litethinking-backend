from decimal import Decimal
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
from .serializer import ProductoSerializer

empresa_repository = DjangoEmpresaRepository()
producto_repository = DjangoProductoRepository()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

