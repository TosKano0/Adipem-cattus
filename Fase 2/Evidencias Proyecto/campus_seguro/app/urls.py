from django.urls import path
from .views import home, formulario_reporte

urlpatterns = [
    path('', home, name="home"),
    path('formulario-reporte/', formulario_reporte, name="formulario-reporte"),
]