from django.contrib import admin
from app.models import Usuario, Reporte, HistorialAsignacion, Categoria, Prioridad, Rol, Genero, Edificio, Piso, Sala
from django.contrib.auth.admin import UserAdmin

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo")
    search_fields = ("nombre", "codigo")

@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "edificio", "numero", "etiqueta")
    list_filter = ("edificio",)
    search_fields = ("etiqueta", "edificio__nombre", "edificio__codigo", "=numero")

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    exclude = ("edificio",)
    autocomplete_fields = ("piso",)
    list_display = ("codigo", "nombre", "edificio", "piso")
    list_filter = ("edificio", "piso")
    search_fields = ("codigo", "nombre", "edificio__nombre", "edificio__codigo")

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Datos adicionales", {"fields": ("edad", "genero", "nombre_rol")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Datos adicionales", {"fields": ("edad", "genero", "nombre_rol")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "nombre_rol", "is_staff")

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    search_fields = ['titulo', 'descripcion', 'ubicacion', 'categoria', 'prioridad']
    list_display = ['titulo', 'estado', 'asignado_a', 'created']

@admin.register(HistorialAsignacion)
class HistorialAsignacionAdmin(admin.ModelAdmin):
    list_display = ('reporte', 'asignado_de', 'asignado_a', 'estado_de', 'estado_a', 'cambiado_por', 'creado_en')
    list_filter = ('estado_a', 'estado_de', 'creado_en')
    search_fields = ('reporte__titulo', 'asignado_de__username', 'asignado_a__username', 'cambiado_por__username')
    autocomplete_fields = ('reporte', 'asignado_de', 'asignado_a', 'cambiado_por')

admin.site.register(Categoria)
admin.site.register(Prioridad)
admin.site.register(Rol)
admin.site.register(Genero)