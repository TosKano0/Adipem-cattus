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
    categoria = forms.ChoiceField(
        choices=CATEGORIAS,
        widget=forms.Select(attrs={"class": "form__control"})
    )
    prioridad = forms.ChoiceField(
        choices=PRIORIDADES,
        widget=forms.Select(attrs={"class": "form__control"})
    )

    edificio = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        required=True,
        label="Edificio",
        widget=forms.Select(attrs={"class": "form__control"})
    )
    piso = forms.ModelChoiceField(
        queryset=Piso.objects.none(),
        required=True,
        label="Piso",
        widget=forms.Select(attrs={"class": "form__control"})
    )

    class Meta:
        model = Reporte
        fields = ["titulo", "categoria", "prioridad", "descripcion", "imagen", "sala"]
        labels = {
            "titulo": "Título",
            "categoria": "Categoría",
            "prioridad": "Prioridad",
            "descripcion": "Descripción",
            "imagen": "Imagen",
            "sala": "Sala",
        }
        help_texts = {
            "descripcion": "Describe el problema con detalles útiles (fechas, personas, etc.).",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form__control",
                "placeholder": "Ej.: Fuga de agua"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form__control",
                "rows": 4,
                "placeholder": "Cuéntanos qué pasa…"
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "form__control",
                "accept": "image/*"
            }),
            "sala": forms.Select(attrs={"class": "form__control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["piso"].queryset = Piso.objects.none()
        self.fields["sala"].queryset = Sala.objects.none()

        if "edificio" in self.data:
            try:
                edificio_id = int(self.data.get("edificio"))
                self.fields["piso"].queryset = Piso.objects.filter(
                    edificio_id=edificio_id
                ).order_by("numero")
            except (ValueError, TypeError):
                pass

        if "piso" in self.data:
            try:
                piso_id = int(self.data.get("piso"))
                self.fields["sala"].queryset = Sala.objects.filter(
                    piso_id=piso_id
                ).order_by("codigo")
            except (ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.sala_id:
            sala = self.instance.sala
            # Prellenar edificio y piso
            self.fields["edificio"].initial = sala.edificio
            self.fields["piso"].queryset = Piso.objects.filter(
                edificio=sala.edificio
            ).order_by("numero")
            self.fields["piso"].initial = sala.piso
            self.fields["sala"].queryset = Sala.objects.filter(
                piso=sala.piso
            ).order_by("codigo")

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

    def __init__(self, *args, **kwargs):
        # ⬅️ Recibimos el usuario que está creando la cuenta
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        # Valor por defecto del rol
        self.fields["nombre_rol"].initial = "usuario"

        # Usamos los choices declarados en el modelo Usuario
        if hasattr(User, "ROL_CHOICES"):
            self.fields["nombre_rol"].choices = User.ROL_CHOICES

        # ¿El que registra es admin?
        es_admin = False
        if self.request_user and self.request_user.is_authenticated:
            es_admin = (
                self.request_user.is_superuser
                or self.request_user.is_staff
                or getattr(self.request_user, "nombre_rol", None) == "administracion"
            )

        if not es_admin:
            # 🚫 No admin: no puede cambiar el rol
            self.fields["nombre_rol"].choices = [("usuario", "Usuario")]
            self.fields["nombre_rol"].disabled = True  # Lo ve pero bloqueado


    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").lower()
        if not email.endswith("@duocuc.cl"):
            raise forms.ValidationError("El correo debe ser @duocuc.cl")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # username = correo
        email = self.cleaned_data["email"].lower()
        user.username = email
        user.email = email

        # Revalidamos si el creador es admin por seguridad
        es_admin = False
        if self.request_user and self.request_user.is_authenticated:
            es_admin = (
                self.request_user.is_superuser
                or self.request_user.is_staff
                or getattr(self.request_user, "nombre_rol", None) == "administracion"
            )

        if es_admin:
            # ✅ Admin: se respeta lo que eligió en el form (si viene vacío, usuario)
            user.nombre_rol = self.cleaned_data.get("nombre_rol") or "usuario"
        else:
            # 🚫 No admin: siempre será usuario aunque “toqueteen” el HTML
            user.nombre_rol = "usuario"

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