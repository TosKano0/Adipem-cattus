from django.urls import path
from . import views

urlpatterns = [
    # 1.Página inicial → LOGIN
    path("", views.login_view, name="login"),             
    path("login/", views.login_view, name="login_alias"),  

    # 2.Registro de nuevos usuarios
    path("home/", views.home, name="home"),

    # 3.Panel principal tras iniciar sesión
    path("usuario_principal/", views.usuario_principal, name="usuario_principal"),

    # 4.Cierre de sesión
    path("logout/", views.logout_view, name="logout"),

    # 5.Formulario de reportes
    path("formulario-reporte/", views.formulario_reporte, name="formulario_reporte"),
]
