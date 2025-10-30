from django.contrib import admin
from app.models import Reporte
from app.models import RegistroUsuario, Categoria, Prioridad, Rol, Genero, Edificio, Piso, Sala

# --- Edificio (opcional, básico) ---
@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo")
    search_fields = ("nombre", "codigo")


# --- Piso: NECESARIO para el autocomplete de Sala ---
@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "edificio", "numero", "etiqueta")
    list_filter = ("edificio",)
    # OJO: '=numero' por ser IntegerField
    search_fields = ("etiqueta", "edificio__nombre", "edificio__codigo", "=numero")


# --- Sala: ocultamos edificio y usamos autocomplete para piso ---
@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    exclude = ("edificio",)              # edificio se setea en Sala.save() según el piso
    autocomplete_fields = ("piso",)
    list_display = ("codigo", "nombre", "edificio", "piso")
    list_filter = ("edificio", "piso")
    search_fields = ("codigo", "nombre", "edificio__nombre", "edificio__codigo")

admin.site.register(Reporte)
admin.site.register(RegistroUsuario)
admin.site.register(Categoria)
admin.site.register(Prioridad)
admin.site.register(Rol)
admin.site.register(Genero)