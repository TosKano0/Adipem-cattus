from django import forms
from app.models import Reporte, Categoria, Prioridad, Rol, Genero, Edificio, Piso, Sala
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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

User = get_user_model()

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre", max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"})
    )
    last_name = forms.CharField(
        label="Apellido", max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "tucorreo@duocuc.cl"})
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "edad", "genero", "nombre_rol")
        widgets = {
            "edad":       forms.NumberInput(attrs={"class": "form-control", "min": 0, "placeholder": "Tu edad"}),
            "genero":     forms.Select(attrs={"class": "form-select"}),
            "nombre_rol": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").lower()
        if not email.endswith("@duocuc.cl"):
            raise forms.ValidationError("El correo debe ser @duocuc.cl")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].lower()
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user

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