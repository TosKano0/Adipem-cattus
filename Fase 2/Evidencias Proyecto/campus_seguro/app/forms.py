# app/forms.py
from django import forms
from .models import Reporte, RegistroUsuario, Categoria, Prioridad, Rol, Genero, Edificio, Piso, Sala

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
        if img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La imagen no puede superar 5MB.")
        if hasattr(img, "content_type") and not img.content_type.startswith("image/"):
            raise forms.ValidationError("El archivo debe ser una imagen válida.")
        return img


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña *", "class": "form-control"}),
        min_length=6
    )

    class Meta:
        model = RegistroUsuario
        fields = ["nombre", "apellido", "email", "password", "edad", "genero", "nombre_rol"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre *", "class": "form-control"}),
            "apellido": forms.TextInput(attrs={"placeholder": "Apellido *", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Correo electrónico *", "class": "form-control"}),
            "edad": forms.NumberInput(attrs={"min": 16, "max": 99, "placeholder": "Edad *", "class": "form-control"}),
            "genero": forms.Select(attrs={"class": "form-select"}),
            "nombre_rol": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Este campo es obligatorio.")
        if not (email.endswith("@duocuc.cl") or email.endswith("@mantenimiento.cl")):
            raise forms.ValidationError("El correo debe ser de dominio @duocuc.cl o @mantenimiento.cl en caso de ser empleado de mantenimiento.")
        return email


# Formularios de administración
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class PrioridadForm(forms.ModelForm):
    class Meta:
        model = Prioridad
        fields = ['nivel']

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre_rol']

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['genero']

class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'codigo']

class PisoForm(forms.ModelForm):
    class Meta:
        model = Piso
        fields = ['edificio', 'numero', 'etiqueta']

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['piso', 'codigo', 'nombre']