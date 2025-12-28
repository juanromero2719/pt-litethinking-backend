"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

from litethinking.presentation.api.auth.views import LoginView, RefreshTokenView
from litethinking.presentation.api.empresa.views import (
    empresa_detail,
    empresas_list_create,
)
from litethinking.presentation.api.inventario.views import generar_inventario_pdf
from litethinking.presentation.api.producto.views import (
    producto_agregar_precio,
    producto_detail,
    productos_list_create,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Autenticación
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("api/auth/login", LoginView.as_view(), name="login_no_slash"),
    path("api/auth/refresh", RefreshTokenView.as_view(), name="refresh_token_no_slash"),
    # Empresas
    path("api/empresas/", empresas_list_create, name="empresas_list_create"),
    path("api/empresas", empresas_list_create, name="empresas_list_create_no_slash"),
    path("api/empresas/<str:nit>/", empresa_detail, name="empresa_detail"),
    path("api/empresas/<str:nit>", empresa_detail, name="empresa_detail_no_slash"),
    # Productos
    path("api/productos/", productos_list_create, name="productos_list_create"),
    path("api/productos", productos_list_create, name="productos_list_create_no_slash"),
    path("api/productos/<str:codigo>/", producto_detail, name="producto_detail"),
    path("api/productos/<str:codigo>", producto_detail, name="producto_detail_no_slash"),
    path("api/productos/<str:codigo>/precios/", producto_agregar_precio, name="producto_agregar_precio"),
    path("api/productos/<str:codigo>/precios", producto_agregar_precio, name="producto_agregar_precio_no_slash"),
    # Inventario PDF
    path("api/inventario/empresa/<str:empresa_nit>/pdf/", generar_inventario_pdf, name="generar_inventario_pdf"),
    path("api/inventario/empresa/<str:empresa_nit>/pdf", generar_inventario_pdf, name="generar_inventario_pdf_no_slash"),
]
