from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....application.use_cases.empresa_use_cases import (
    ActualizarEmpresaUseCase,
    CrearEmpresaUseCase,
    EliminarEmpresaUseCase,
    ListarEmpresasUseCase,
    ObtenerEmpresaUseCase,
)
from ....infrastructure.persistence.empresa.repository_impl import DjangoEmpresaRepository
from .serializer import EmpresaSerializer

empresa_repository = DjangoEmpresaRepository()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def empresas_list_create(request):
    if request.method == 'GET':
        use_case = ListarEmpresasUseCase(empresa_repository)
        empresas = use_case.ejecutar()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':

        serializer = EmpresaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            use_case = CrearEmpresaUseCase(empresa_repository)
            empresa = use_case.ejecutar(
                nit=serializer.validated_data['nit'],
                nombre=serializer.validated_data['nombre'],
                direccion=serializer.validated_data['direccion'],
                telefono=serializer.validated_data['telefono'],
            )
            response_serializer = EmpresaSerializer(empresa)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def empresa_detail(request, nit):
    if request.method == 'GET':
        use_case = ObtenerEmpresaUseCase(empresa_repository)
        empresa = use_case.ejecutar(nit)
        if not empresa:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Validar datos de entrada con el serializer
        serializer = EmpresaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            use_case = ActualizarEmpresaUseCase(empresa_repository)
            empresa = use_case.ejecutar(
                nit=nit,
                nombre=serializer.validated_data['nombre'],
                direccion=serializer.validated_data['direccion'],
                telefono=serializer.validated_data['telefono'],
            )
            response_serializer = EmpresaSerializer(empresa)
            return Response(response_serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        use_case = EliminarEmpresaUseCase(empresa_repository)
        eliminado = use_case.ejecutar(nit)
        if not eliminado:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

