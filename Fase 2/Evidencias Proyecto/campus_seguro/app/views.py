from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReporteForm, RegistroUsuarioForm  

# Create your views here.
def formulario_reporte(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Reporte creado con éxito.")
            return redirect("home")  # o a una lista/detalle
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
            messages.success(request, "✅ Usuario registrado correctamente.")
            return redirect("home")
        else:
            messages.error(request, "⚠️ Revisa los campos marcados.")
    else:
        form = RegistroUsuarioForm()

    return render(request, "app/home.html", {"form": form})
