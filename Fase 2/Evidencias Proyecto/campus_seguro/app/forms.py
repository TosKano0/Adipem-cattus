# app/forms.py
from django import forms
from .models import Reporte

CATEGORIAS = [
    ("Infraestructura", "Infraestructura"),
    ("Limpieza", "Limpieza"),
    ("Tecnología", "Tecnología"),
]

PRIORIDADES = [
    ("Baja", "Baja"),
    ("Media", "Media"),
    ("Alta", "Alta"),
]

class ReporteForm(forms.ModelForm):
    categoria = forms.ChoiceField(choices=CATEGORIAS)
    prioridad = forms.ChoiceField(choices=PRIORIDADES)

    class Meta:
        model = Reporte
        fields = ["titulo", "ubicacion", "categoria", "prioridad", "descripcion", "imagen"]
        labels = {
            "titulo": "Título",
            "ubicacion": "Ubicación",
            "categoria": "Categoría",
            "prioridad": "Prioridad",
            "descripcion": "Descripción",
            "imagen": "Imagen"
        }
        help_texts = {
            "descripcion": "Describe el problema con detalles útiles (fechas, personas, etc.).",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form__control", "placeholder": "Ej.: Fuga de agua"}),
            "ubicacion": forms.TextInput(attrs={"class": "form__control", "placeholder": "Ej.: Edificio E - Sala 104"}),
            "categoria": forms.Select(attrs={"class": "form__control"}),
            "prioridad": forms.Select(attrs={"class": "form__control"}),
            "descripcion": forms.Textarea(attrs={"class": "form__control", "rows": 4, "placeholder": "Cuéntanos qué pasa…"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form__control", "accept": "image/*"}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 4:
            raise forms.ValidationError("El título debe tener al menos 4 caracteres.")
        return titulo

    def clean_imagen(self):
        img = self.cleaned_data.get("imagen")
        if not img:
            return img
        # Tamaño máx ~5MB
        if img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La imagen no puede superar 5MB.")
        # Tipo básico
        if hasattr(img, "content_type") and not img.content_type.startswith("image/"):
            raise forms.ValidationError("El archivo debe ser una imagen válida.")
        return img