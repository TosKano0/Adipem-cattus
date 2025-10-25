from django.urls import path
from .views import home, usuario_principal, formulario_reporte

urlpatterns = [
    path('', home, name="home"),
    path('formulario-reporte/', formulario_reporte, name="formulario-reporte"),
    path('usuario_principal/', usuario_principal, name="usuario_principal"),
]



# Página login Ultima Actualizacion Jordan no borrar este cuadro

from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),  # Página de registro
    path("login/", views.login_view, name="login"),  # Login
    path("usuario_principal/", views.usuario_principal, name="usuario_principal"),  # Dashboard
    path("logout/", views.logout_view, name="logout"),  # Cerrar sesión
]

# Página login Ultima Actualizacion Jordan no borrar este cuadro