from django.urls import path
from . import views
from app.views import home, usuario_principal, formulario_reporte, admin, asignar_mantenedor, panel_admin, panel_admin_ubicacion, ReporteListView, ReporteCreateView, ReporteUpdateView, ReporteDeleteView, UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, PrioridadListView, PrioridadCreateView, PrioridadUpdateView, PrioridadDeleteView, RolListView, RolCreateView, RolUpdateView, RolDeleteView, GeneroListView, GeneroCreateView, GeneroUpdateView, GeneroDeleteView, EdificioListView, EdificioCreateView, EdificioUpdateView, EdificioDeleteView, PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView, SalaListView, SalaCreateView, SalaUpdateView, SalaDeleteView, cargar_pisos, cargar_salas

urlpatterns = [
    # 1. Página inicial → LOGIN
    path("", views.login_view, name="login"),             
    path("login/", views.login_view, name="login_alias"),  

    # 2. Registro de nuevos usuarios
    path("home/", views.home, name="home"),

    # 3. Panel principal tras iniciar sesión
    path("usuario_principal/", views.usuario_principal, name="usuario_principal"),

    # 4. Dashboard de mantenimiento
    path("mantenimiento_dashboard/", views.mantenimiento, name="mantenimiento"),

    # 5. NUEVO: Actualizar estado de reporte (para el formulario en el template)
    path("mantenimiento/actualizar-estado/", views.actualizar_estado_reporte, name="actualizar_estado_reporte"),

    # 4. Cierre de sesión
    path("logout/", views.logout_view, name="logout"),

    # 5. Formulario de reportes
    path('formulario-reporte/', formulario_reporte, name="formulario-reporte"),
    
    path('administrador/', admin, name="admin"),
    
    path('administrador/reportes/<int:pk>/asignar/', asignar_mantenedor, name="asignar-mantenedor"),
    
    path('administrador/panel/', panel_admin, name="panel-admin"),
    
    path('administrador/panel/ubicacion', panel_admin_ubicacion, name="panel-admin-ubicacion"),

    # Configuración de géneros
    path("administrador/panel/generos/", GeneroListView.as_view(), name="genero-list"),
    path("administrador/panel/generos/nuevo/", GeneroCreateView.as_view(), name="genero-create"),
    path("administrador/panel/generos/<int:pk>/editar/", GeneroUpdateView.as_view(), name="genero-update"),
    path("administrador/panel/generos/<int:pk>/eliminar/", GeneroDeleteView.as_view(), name="genero-delete"),
    
    # Configuración de categorías
    path("administrador/panel/categorias/", CategoriaListView.as_view(), name="categoria-list"),
    path("administrador/panel/categorias/nuevo/", CategoriaCreateView.as_view(), name="categoria-create"),
    path("administrador/panel/categorias/<int:pk>/editar/", CategoriaUpdateView.as_view(), name="categoria-update"),
    path("administrador/panel/categorias/<int:pk>/eliminar/", CategoriaDeleteView.as_view(), name="categoria-delete"),
    
    # Configuración de prioridades
    path("administrador/panel/prioridades/", PrioridadListView.as_view(), name="prioridad-list"),
    path("administrador/panel/prioridades/nuevo/", PrioridadCreateView.as_view(), name="prioridad-create"),
    path("administrador/panel/prioridades/<int:pk>/editar/", PrioridadUpdateView.as_view(), name="prioridad-update"),
    path("administrador/panel/prioridades/<int:pk>/eliminar/", PrioridadDeleteView.as_view(), name="prioridad-delete"),
    
    # Configuración de roles
    path("administrador/panel/roles/", RolListView.as_view(), name="rol-list"),
    path("administrador/panel/roles/nuevo/", RolCreateView.as_view(), name="rol-create"),
    path("administrador/panel/roles/<int:pk>/editar/", RolUpdateView.as_view(), name="rol-update"),
    path("administrador/panel/roles/<int:pk>/eliminar/", RolDeleteView.as_view(), name="rol-delete"),
    
    # Edificios
    path("administrador/panel/ubicacion/edificios/", EdificioListView.as_view(), name="edificio-list"),
    path("administrador/panel/ubicacion/edificios/nuevo/", EdificioCreateView.as_view(), name="edificio-create"),
    path("administrador/panel/ubicacion/edificios/<int:pk>/editar/", EdificioUpdateView.as_view(), name="edificio-update"),
    path("administrador/panel/ubicacion/edificios/<int:pk>/eliminar/", EdificioDeleteView.as_view(), name="edificio-delete"),

    # Pisos
    path("administrador/panel/ubicacion/pisos/", PisoListView.as_view(), name="piso-list"),
    path("administrador/panel/ubicacion/pisos/nuevo/", PisoCreateView.as_view(), name="piso-create"),
    path("administrador/panel/ubicacion/pisos/<int:pk>/editar/", PisoUpdateView.as_view(), name="piso-update"),
    path("administrador/panel/ubicacion/pisos/<int:pk>/eliminar/", PisoDeleteView.as_view(), name="piso-delete"),

    # Salas
    path("administrador/panel/ubicacion/salas/", SalaListView.as_view(), name="sala-list"),
    path("administrador/panel/ubicacion/salas/nuevo/", SalaCreateView.as_view(), name="sala-create"),
    path("administrador/panel/ubicacion/salas/<int:pk>/editar/", SalaUpdateView.as_view(), name="sala-update"),
    path("administrador/panel/ubicacion/salas/<int:pk>/eliminar/", SalaDeleteView.as_view(), name="sala-delete"),
    
    # Reportes
    path("administrador/panel/reportes/", ReporteListView.as_view(), name="reporte-list"),
    path("administrador/panel/reportes/nuevo/", ReporteCreateView.as_view(), name="reporte-create"),
    path("administrador/panel/reportes/<int:pk>/editar/", ReporteUpdateView.as_view(), name="reporte-update"),
    path("administrador/panel/reportes/<int:pk>/eliminar/", ReporteDeleteView.as_view(), name="reporte-delete"),
    
    # Usuarios
    path("administrador/panel/usuarios/", UsuarioListView.as_view(), name="usuario-list"),
    path("administrador/panel/usuarios/nuevo/", UsuarioCreateView.as_view(), name="usuario-create"),
    path("administrador/panel/usuarios/<int:pk>/editar/", UsuarioUpdateView.as_view(), name="usuario-update"),
    path("administrador/panel/usuarios/<int:pk>/eliminar/", UsuarioDeleteView.as_view(), name="usuario-delete"),
    
    path("api/pisos/", cargar_pisos, name="cargar-pisos"),
    path("api/salas/", cargar_salas, name="cargar-salas"),
]
