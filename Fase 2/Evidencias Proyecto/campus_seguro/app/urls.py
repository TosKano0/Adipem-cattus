from django.urls import path
from .views import home, usuario_principal, formulario_reporte, administrador

urlpatterns = [
    path('', home, name="home"),
    path('formulario-reporte/', formulario_reporte, name="formulario-reporte"),
    path('usuario_principal/', usuario_principal, name="usuario_principal"),
    path('administrador/', administrador, name="adminimintrador"),
]
