"""
URL configuration for campus_seguro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# ==============================
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro


from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Página inicial: LOGIN (vista principal al abrir el servidor)
    path("", views.login_view, name="login_principal"),

    # Alias explícito si quieres seguir accediendo a /login/
    path("login/", views.login_view, name="login"),

    # Página de registro (home)
    path("home/", views.home, name="home"),

    # Pantalla principal después de iniciar sesión
    path("usuario_principal/", views.usuario_principal, name="usuario_principal"),

    # Cierre de sesión
    path("logout/", views.logout_view, name="logout"),
]




# ==============================
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro