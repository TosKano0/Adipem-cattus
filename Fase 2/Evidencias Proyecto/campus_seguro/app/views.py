from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReporteForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

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