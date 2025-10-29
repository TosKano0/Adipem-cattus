from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import RegistroUsuario
from .forms import RegistroUsuarioForm, ReporteForm



# 1 REGISTRO DE NUEVO USUARIO (home.html)

def home(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data["password"])
            usuario.save()
            messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            return redirect("login")  # 🔧 Cambio: redirige al login
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, "app/home.html", {"form": form})



# 2 INICIO DE SESIÓN (login.html)

def login_view(request):
    """
    Vista de inicio de sesión.
    Si el usuario ya tiene sesión activa, lo redirige al panel principal.
    """
    # Evita que usuarios ya logueados vuelvan al login
    if request.session.get("usuario_id"):
        return redirect("usuario_principal")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            usuario = RegistroUsuario.objects.get(email=email)
        except RegistroUsuario.DoesNotExist:
            messages.error(request, "El usuario no existe o el correo es incorrecto.")
            return render(request, "app/login.html")

        # validación de contraseña y creación de sesión
        if check_password(password, usuario.password):
            request.session["usuario_id"] = usuario.id
            request.session["usuario_nombre"] = usuario.nombre
            messages.success(request, f"Bienvenido {usuario.nombre} 👋")
            return redirect("usuario_principal")
        else:
            messages.error(request, "Contraseña incorrecta. Intenta nuevamente.")

    return render(request, "app/login.html")



# 3 PANEL PRINCIPAL (usuario_principal.html)

def usuario_principal(request):
    usuario_id = request.session.get("usuario_id")

    # protección si no hay sesión activa
    if not usuario_id:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    usuario = RegistroUsuario.objects.get(id=usuario_id)
    return render(request, "app/usuario_principal.html", {"usuario": usuario})



# 4 CERRAR SESIÓN

def logout_view(request):
    """
    Cierra la sesión actual y redirige al login.
    """
    request.session.flush()  # 
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("login")  # 



# 5 FORMULARIO DE REPORTE 

def formulario_reporte(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Reporte creado con éxito.")
            return redirect("usuario_principal")
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = ReporteForm()
    return render(request, "app/form_reporte.html", {"form": form})
