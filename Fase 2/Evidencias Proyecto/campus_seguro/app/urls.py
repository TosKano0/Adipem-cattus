from django.urls import path
from . import views
<<<<<<< HEAD
from .views import home, usuario_principal, mantenimiento_dashboard, formulario_reporte, administrador, admin_ubicacion, CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, PrioridadListView, PrioridadCreateView, PrioridadUpdateView, PrioridadDeleteView, RolListView, RolCreateView, RolUpdateView, RolDeleteView, GeneroListView, GeneroCreateView, GeneroUpdateView, GeneroDeleteView, EdificioListView, EdificioCreateView, EdificioUpdateView, EdificioDeleteView, PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView, SalaListView, SalaCreateView, SalaUpdateView, SalaDeleteView
=======
from .views import home, usuario_principal, formulario_reporte, administrador, admin_ubicacion, CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, PrioridadListView, PrioridadCreateView, PrioridadUpdateView, PrioridadDeleteView, RolListView, RolCreateView, RolUpdateView, RolDeleteView, GeneroListView, GeneroCreateView, GeneroUpdateView, GeneroDeleteView, EdificioListView, EdificioCreateView, EdificioUpdateView, EdificioDeleteView, PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView, SalaListView, SalaCreateView, SalaUpdateView, SalaDeleteView
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d

urlpatterns = [
    # 1. Página inicial → LOGIN
    path("", views.login_view, name="login"),             
    path("login/", views.login_view, name="login_alias"),  

    # 2. Registro de nuevos usuarios
    path("home/", views.home, name="home"),

    # 3. Panel principal tras iniciar sesión
    path("usuario_principal/", views.usuario_principal, name="usuario_principal"),

    # 👇 NUEVO: Dashboard de mantenimiento
    path("mantenimiento_dashboard/", views.mantenimiento_dashboard, name="mantenimiento_dashboard"),

    # 4. Cierre de sesión
    path("logout/", views.logout_view, name="logout"),

<<<<<<< HEAD
    # 5. Formulario de reportes
    path('formulario-reporte/', views.formulario_reporte, name="formulario-reporte"),
    
    # Rutas duplicadas (puedes eliminar una si lo deseas, pero no causan error)
=======
    # 5.Formulario de reportes
    path('formulario-reporte/', views.formulario_reporte, name="formulario-reporte"),
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path('usuario_principal/', usuario_principal, name="usuario_principal"),
    path('administrador/', administrador, name="administrador"),
    path('administrador/ubicacion', admin_ubicacion, name="admin-ubicacion"),

<<<<<<< HEAD
    # Configuración de generos
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/generos/", GeneroListView.as_view(), name="genero-list"),
    path("administrador/generos/nuevo/", GeneroCreateView.as_view(), name="genero-create"),
    path("administrador/generos/<int:pk>/editar/", GeneroUpdateView.as_view(), name="genero-update"),
    path("administrador/generos/<int:pk>/eliminar/", GeneroDeleteView.as_view(), name="genero-delete"),
    
<<<<<<< HEAD
    # Configuración de categorías
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/categorias/", CategoriaListView.as_view(), name="categoria-list"),
    path("administrador/categorias/nuevo/", CategoriaCreateView.as_view(), name="categoria-create"),
    path("administrador/categorias/<int:pk>/editar/", CategoriaUpdateView.as_view(), name="categoria-update"),
    path("administrador/categorias/<int:pk>/eliminar/", CategoriaDeleteView.as_view(), name="categoria-delete"),
    
<<<<<<< HEAD
    # Configuración de prioridades
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/prioridades/", PrioridadListView.as_view(), name="prioridad-list"),
    path("administrador/prioridades/nuevo/", PrioridadCreateView.as_view(), name="prioridad-create"),
    path("administrador/prioridades/<int:pk>/editar/", PrioridadUpdateView.as_view(), name="prioridad-update"),
    path("administrador/prioridades/<int:pk>/eliminar/", PrioridadDeleteView.as_view(), name="prioridad-delete"),
    
<<<<<<< HEAD
    # Configuración de roles
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/roles/", RolListView.as_view(), name="rol-list"),
    path("administrador/roles/nuevo/", RolCreateView.as_view(), name="rol-create"),
    path("administrador/roles/<int:pk>/editar/", RolUpdateView.as_view(), name="rol-update"),
    path("administrador/roles/<int:pk>/eliminar/", RolDeleteView.as_view(), name="rol-delete"),
    
<<<<<<< HEAD
    # Edificios
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/ubicacion/edificios/", EdificioListView.as_view(), name="edificio-list"),
    path("administrador/ubicacion/edificios/nuevo/", EdificioCreateView.as_view(), name="edificio-create"),
    path("administrador/ubicacion/edificios/<int:pk>/editar/", EdificioUpdateView.as_view(), name="edificio-update"),
    path("administrador/ubicacion/edificios/<int:pk>/eliminar/", EdificioDeleteView.as_view(), name="edificio-delete"),

<<<<<<< HEAD
    # Pisos
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/ubicacion/pisos/", PisoListView.as_view(), name="piso-list"),
    path("administrador/ubicacion/pisos/nuevo/", PisoCreateView.as_view(), name="piso-create"),
    path("administrador/ubicacion/pisos/<int:pk>/editar/", PisoUpdateView.as_view(), name="piso-update"),
    path("administrador/ubicacion/pisos/<int:pk>/eliminar/", PisoDeleteView.as_view(), name="piso-delete"),

<<<<<<< HEAD
    # Salas
=======
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
    path("administrador/ubicacion/salas/", SalaListView.as_view(), name="sala-list"),
    path("administrador/ubicacion/salas/nuevo/", SalaCreateView.as_view(), name="sala-create"),
    path("administrador/ubicacion/salas/<int:pk>/editar/", SalaUpdateView.as_view(), name="sala-update"),
    path("administrador/ubicacion/salas/<int:pk>/eliminar/", SalaDeleteView.as_view(), name="sala-delete"),
<<<<<<< HEAD
]
=======
]
>>>>>>> 052c79428d73e0175c241cf6c7bb420c83ff567d
