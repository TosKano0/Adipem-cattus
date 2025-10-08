from django import forms
from .models import RegistroUsuario

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña *"}),
        min_length=6
    )

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
