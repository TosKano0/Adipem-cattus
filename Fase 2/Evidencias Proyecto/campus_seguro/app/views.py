from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'app/home.html')


# app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm  

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
