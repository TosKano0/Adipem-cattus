from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PisoForm, ReporteForm, RegistroUsuarioForm, CategoriaForm, PrioridadForm, RolForm, GeneroForm, EdificioForm, SalaForm
from .models import Usuario, Genero, Prioridad, Rol, Categoria, Edificio, Piso, Sala
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Reporte
from .forms import RegistroUsuarioForm, ReporteForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# 1 REGISTRO DE NUEVO USUARIO (home.html)
def home(request):
    if request.user.is_authenticated:
        return redirect("usuario_principal")

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente. Ahora puedes iniciar sesión.")
            return redirect("login")
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = RegistroUsuarioForm()

    return render(request, "app/home.html", {"form": form})

# 2 INICIO DE SESIÓN (login.html)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("usuario_principal")

    if request.method == "POST":
        identificador = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        user = None

        # 1) Intenta autenticar asumiendo que el identificador es el username
        user = authenticate(request, username=identificador, password=password)

        if user is None:
            # 2) Si no funcionó, intenta tratar el identificador como EMAIL
            u = User.objects.filter(email__iexact=identificador).first()
            if u:
                user = authenticate(request, username=u.username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f"Bienvenido {user.first_name or user.username} 👋")
            return redirect("usuario_principal")

        messages.error(request, "Credenciales inválidas.")

    return render(request, "app/login.html")


# 3 PANEL PRINCIPAL (usuario_principal.html)
@login_required
def usuario_principal(request):
    reportes = Reporte.objects.filter(usuario=request.user).order_by('-created')

    paginator = Paginator(reportes, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "app/usuario_principal.html", {
        "reportes": page_obj,
        "page_obj": page_obj
    })

# 4 CERRAR SESIÓN
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("login")

# 5 FORMULARIO DE REPORTE
@login_required
def formulario_reporte(request):
    if request.method == "POST":
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, "Reporte creado con éxito.")
            return redirect("usuario_principal")
        messages.error(request, "Revisa los errores del formulario.")
    else:
        form = ReporteForm()

    return render(request, "app/form_reporte.html", {"form": form})

def administrador(request):
    return render(request, "app/administrador.html")

def admin_ubicacion(request):
    return render(request, "app/admin_ubicacion.html")

class CategoriaListView(ListView):
    model = Categoria
    paginate_by = 10
    template_name = "app/list_categoria.html"

class PrioridadListView(ListView):
    model = Prioridad
    paginate_by = 10
    template_name = "app/list_prioridad.html"

class RolListView(ListView):
    model = Rol
    paginate_by = 10
    template_name = "app/list_rol.html"

class GeneroListView(ListView):
    model = Genero
    paginate_by = 10
    template_name = "app/list_genero.html"

class EdificioListView(ListView):
    model = Edificio
    paginate_by = 10
    template_name = "app/list_edificio.html"

class PisoListView(ListView):
    model = Piso
    paginate_by = 10
    template_name = "app/list_piso.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("edificio")
        b = self.request.GET.get("edificio")
        if b:
            qs = qs.filter(edificio__id=b)
        return qs

class SalaListView(ListView):
    model = Sala
    paginate_by = 10
    template_name = "app/list_sala.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("edificio", "piso", "piso__edificio")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q) | Q(edificio__nombre__icontains=q) | Q(piso__etiqueta__icontains=q))
        return qs

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "app/form_categoria.html"
    success_url = reverse_lazy("categoria-list")

class PrioridadCreateView(CreateView):
    model = Prioridad
    form_class = PrioridadForm
    template_name = "app/form_prioridad.html"
    success_url = reverse_lazy("prioridad-list")

class RolCreateView(CreateView):
    model = Rol
    form_class = RolForm
    template_name = "app/form_rol.html"
    success_url = reverse_lazy("rol-list")

class GeneroCreateView(CreateView):
    model = Genero
    form_class = GeneroForm
    template_name = "app/form_genero.html"
    success_url = reverse_lazy("genero-list")

class EdificioCreateView(CreateView):
    model = Edificio
    form_class = EdificioForm
    template_name = "app/form_edificio.html"
    success_url = reverse_lazy("edificio-list")

class PisoCreateView(CreateView):
    model = Piso
    form_class = PisoForm
    template_name = "app/form_piso.html"
    success_url = reverse_lazy("piso-list")

class SalaCreateView(CreateView):
    model = Sala
    form_class = SalaForm
    template_name = "app/form_sala.html"
    success_url = reverse_lazy("sala-list")

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "app/form_categoria.html"
    success_url = reverse_lazy("categoria-list")

class PrioridadUpdateView(UpdateView):
    model = Prioridad
    form_class = PrioridadForm
    template_name = "app/form_prioridad.html"
    success_url = reverse_lazy("prioridad-list")

class RolUpdateView(UpdateView):
    model = Rol
    form_class = RolForm
    template_name = "app/form_rol.html"
    success_url = reverse_lazy("rol-list")

class GeneroUpdateView(UpdateView):
    model = Genero
    form_class = GeneroForm
    template_name = "app/form_genero.html"
    success_url = reverse_lazy("genero-list")

class EdificioUpdateView(UpdateView):
    model = Edificio
    form_class = EdificioForm
    template_name = "app/form_edificio.html"
    success_url = reverse_lazy("edificio-list")

class PisoUpdateView(UpdateView):
    model = Piso
    form_class = PisoForm
    template_name = "app/form_piso.html"
    success_url = reverse_lazy("piso-list")

class SalaUpdateView(UpdateView):
    model = Sala
    form_class = SalaForm
    template_name = "app/form_sala.html"
    success_url = reverse_lazy("sala-list")

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("categoria-list")

class PrioridadDeleteView(DeleteView):
    model = Prioridad
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("prioridad-list")

class RolDeleteView(DeleteView):
    model = Rol
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("rol-list")

class GeneroDeleteView(DeleteView):
    model = Genero
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("genero-list")

class EdificioDeleteView(DeleteView):
    model = Edificio
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("edificio-list")

class PisoDeleteView(DeleteView):
    model = Piso
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("piso-list")

class SalaDeleteView(DeleteView):
    model = Sala
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("sala-list")
