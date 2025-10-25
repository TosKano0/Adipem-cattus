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
            return redirect("usuario_principal")  
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



# ==============================
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro
   # Página login Ultima Actualizacion Jordan no borrar este cuadro



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import RegistroUsuario
from .forms import RegistroUsuarioForm

# === Registro de usuario ===
def home(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Encriptar la contraseña antes de guardar
            usuario.password = make_password(form.cleaned_data["password"])
            usuario.save()
            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")  # Redirige a la página de login
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroUsuarioForm()

    return render(request, "app/home.html", {"form": form})


# === Inicio de sesión ===
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            usuario = RegistroUsuario.objects.get(email=email)
        except RegistroUsuario.DoesNotExist:
            messages.error(request, "El usuario no existe o el correo es incorrecto.")
            return render(request, "app/login.html")

        # Validar contraseña
        if check_password(password, usuario.password):
            request.session["usuario_id"] = usuario.id
            request.session["usuario_nombre"] = usuario.nombre
            messages.success(request, f"Bienvenido, {usuario.nombre} 👋")
            return redirect("usuario_principal")  # Redirige al dashboard
        else:
            messages.error(request, "Contraseña incorrecta. Inténtalo nuevamente.")

    return render(request, "app/login.html")


# === Página principal tras login ===
def usuario_principal(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    usuario = RegistroUsuario.objects.get(id=usuario_id)
    return render(request, "app/usuario_principal.html", {"usuario": usuario})


# === Cerrar sesión ===
def logout_view(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("login")
