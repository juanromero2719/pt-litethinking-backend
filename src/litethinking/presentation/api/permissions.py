from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name='Admin').exists()

class IsAdminOrExterno(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name__in=['Admin', 'Externo']).exists()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=['Admin', 'Externo']).exists()
        
        return request.user.groups.filter(name='Admin').exists()

