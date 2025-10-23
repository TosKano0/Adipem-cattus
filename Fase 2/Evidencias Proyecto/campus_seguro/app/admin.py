from django.contrib import admin
from app.models import Reporte
from app.models import RegistroUsuario, Categoria, Prioridad, Rol, Genero

# Register your models here.
admin.site.register(Reporte)
admin.site.register(RegistroUsuario)
admin.site.register(Categoria)
admin.site.register(Prioridad)
admin.site.register(Rol)
admin.site.register(Genero)