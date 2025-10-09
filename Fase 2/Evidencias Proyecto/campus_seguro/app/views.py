from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReporteForm, RegistroUsuarioForm
from .models import RegistroUsuario

# Create your views here.
def formulario_reporte(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Reporte creado con éxito.")
            return redirect("usuario_principal")  # o a una lista/detalle
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = ReporteForm()
    return render(request, 'app/form_reporte.html', {"form": form})

def home(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect("usuario_principal")
        else:
            messages.error(request, "Revisa los campos marcados.")
    else:
        form = RegistroUsuarioForm()

    return render(request, "app/home.html", {"form": form})

def usuario_principal(request):
    # Obtener el último usuario registrado
    usuario = RegistroUsuario.objects.last()
    return render(request, "app/usuario_principal.html", {"usuario": usuario})
