from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializer import RegistroSerializer


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            from django.contrib.auth import authenticate
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                grupos = user.groups.all()
                rol = grupos.first().name if grupos.exists() else None
                
                response.data['rol'] = rol
        
        return response


class RefreshTokenView(TokenRefreshView):
    pass


@api_view(['POST'])
def registro(request):

    serializer = RegistroSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario = serializer.save()
        
        try:
            grupo_externo = Group.objects.get(name='Externo')
            usuario.groups.add(grupo_externo)
        except Group.DoesNotExist:
            grupo_externo = Group.objects.create(name='Externo')
            usuario.groups.add(grupo_externo)
        
        return Response(
            {
                'message': 'Usuario registrado exitosamente',
                'username': usuario.username,
                'email': usuario.email,
                'rol': 'Externo'
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'error': f'Error al crear el usuario: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

