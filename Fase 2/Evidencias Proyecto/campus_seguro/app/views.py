from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Usuario, Genero, Prioridad, Rol, Categoria, Edificio, Piso, Sala, Reporte
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PisoForm, ReporteForm, RegistroUsuarioForm, CategoriaForm, PrioridadForm, RolForm, GeneroForm, EdificioForm, SalaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps   # 👈 Agregado aquí
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseForbidden

# ===========================================
# DECORADOR DE CONTROL DE ROLES (CORREGIDO)
# ===========================================
def rol_requerido(roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Debes iniciar sesión.")
                return redirect("login")

            if request.user.nombre_rol not in roles_permitidos:
                # ✅ Agregar mensaje SOLO si el usuario no tiene permiso
                messages.error(request, "Acceso denegado: no tienes permiso para ver esta página.")
                # Redirección personalizada según el rol actual
                if request.user.nombre_rol == "mantenimiento":
                    return redirect("mantenimiento")
                elif request.user.nombre_rol == "administracion":
                    return redirect("admin")
                else:
                    return redirect("usuario_principal")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador

    ...


# 1 REGISTRO DE NUEVO USUARIO (home.html)
def home(request):
    if request.user.is_authenticated:
        # Redirigir según rol
        if request.user.nombre_rol == "administracion":
            return redirect("admin")
        elif request.user.nombre_rol == "mantenimiento":
            return redirect("mantenimiento")
        else:
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
# ===========================================
#  INICIO DE SESIÓN CON CONTROL DE ROL
# ===========================================
def login_view(request):
    if request.user.is_authenticated:
        # Evita redirigir si el usuario no tiene rol definido o sesión dañada
        if not hasattr(request.user, "nombre_rol") or not request.user.nombre_rol:
            logout(request)
            return redirect("login")

        # Redirección automática según rol
        if request.user.nombre_rol == "administracion":
            return redirect("admin")
        elif request.user.nombre_rol == "mantenimiento":
            return redirect("mantenimiento")
        else:
            return redirect("usuario_principal")


    if request.method == "POST":
        identificador = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""
        user = None

        # Buscar usuario por email
        u = Usuario.objects.filter(email__iexact=identificador).first()
        if u:
            user = authenticate(request, username=u.username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f"Bienvenido {user.first_name or user.username} 👋")

            # Redirección por rol
            if user.nombre_rol == "administracion":
                return redirect("admin")
            elif user.nombre_rol == "mantenimiento":
                return redirect("mantenimiento")
            else:
                return redirect("usuario_principal")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, "app/login.html")


# 3 PANEL PRINCIPAL (usuario_principal.html)
@rol_requerido(["usuario"])
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


# 👇 VISTA CORREGIDA: Dashboard de Mantenimiento
@rol_requerido(["mantenimiento"])
@login_required
def mantenimiento(request):
    # Verifica que el usuario sea de mantenimiento
    if request.user.nombre_rol != "mantenimiento":
        messages.error(request, "Acceso denegado. Solo para personal de mantenimiento.")
        return redirect("usuario_principal")

    # Filtra reportes asignados a este usuario
    reportes = Reporte.objects.filter(asignado_a=request.user).order_by('-created')

    # Búsqueda y filtros
    busqueda = request.GET.get('busqueda', '').strip()
    estado_filtro = request.GET.get('estado', 'todos')
    prioridad_filtro = request.GET.get('prioridad', 'todas')

    if busqueda:
        reportes = reportes.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    if estado_filtro != 'todos':
        reportes = reportes.filter(estado=estado_filtro)
    if prioridad_filtro != 'todas':
        reportes = reportes.filter(prioridad=prioridad_filtro)

    # Contadores
    total = reportes.count()
    pendientes = reportes.filter(estado='pendiente').count()
    en_proceso = reportes.filter(estado='en_proceso').count()
    pausados = reportes.filter(estado='pausado').count()
    completados = reportes.filter(estado='completado').count()

    # Paginación
    paginator = Paginator(reportes, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "reportes": page_obj,
        "page_obj": page_obj,
        "total": total,
        "pendientes": pendientes,
        "en_proceso": en_proceso,
        "pausados": pausados,
        "completados": completados,
        "busqueda": busqueda,
        "estado_filtro": estado_filtro,
        "prioridad_filtro": prioridad_filtro,
    }

    return render(request, "app/mantenimiento_dashboard.html", context)


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



# ===========================================
# Vistas de administración protegidas
# ===========================================

from django.utils.decorators import method_decorator

@rol_requerido(["administracion"])
@login_required
def admin(request): 
    reportes = Reporte.objects.all().order_by('-created')

    # Búsqueda y filtros
    busqueda = request.GET.get('busqueda', '').strip()
    estado_filtro = request.GET.get('estado', 'todos')
    prioridad_filtro = request.GET.get('prioridad', 'todas')
    
    mantenedores = _qs_mantenedores()

    if busqueda:
        reportes = reportes.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    if estado_filtro != 'todos':
        reportes = reportes.filter(estado=estado_filtro)
    if prioridad_filtro != 'todas':
        reportes = reportes.filter(prioridad=prioridad_filtro)

    # Contadores
    total = reportes.count()
    pendientes = reportes.filter(estado='pendiente').count()
    en_proceso = reportes.filter(estado='en_proceso').count()
    pausados = reportes.filter(estado='pausado').count()
    completados = reportes.filter(estado='completado').count()

    # Paginación
    paginator = Paginator(reportes, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "reportes": page_obj,
        "page_obj": page_obj,
        "total": total,
        "pendientes": pendientes,
        "en_proceso": en_proceso,
        "pausados": pausados,
        "completados": completados,
        "busqueda": busqueda,
        "estado_filtro": estado_filtro,
        "prioridad_filtro": prioridad_filtro,
        "mantenedores": mantenedores,
    }
    return render(request, "app/admin.html", context)

def _qs_mantenedores():
    return User.objects.filter(nombre_rol__iexact='mantenimiento', is_active=True).order_by('first_name', 'last_name')

User = get_user_model()

@rol_requerido(["administracion"])
@login_required
def asignar_mantenedor(request, pk):
    # Solo deja asignar a staff/superuser (ajusta si tienes decoradores de rol)
    if not (request.user.is_staff or request.user.is_superuser or request.user.nombre_rol == "administracion"):
        return HttpResponseForbidden("No autorizado")

    reporte = get_object_or_404(Reporte, pk=pk)
    asignado_id = request.POST.get('asignado_a')  # puede venir vacío

    # Validar que el usuario seleccionado efectivamente es 'mantenedor'
    mantenedores = _qs_mantenedores()

    if asignado_id in [None, "", "null"]:
        reporte.asignado_a = None
        reporte.save(update_fields=['asignado_a'])
        asignado_nombre = "Sin asignar"
    else:
        try:
            mantenedor = mantenedores.get(pk=asignado_id)
        except User.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Mantenedor inválido."}, status=400)

        reporte.asignado_a = mantenedor
        # (Opcional) mover a "en_proceso" al asignar
        if reporte.estado == 'pendiente':
            reporte.estado = 'en_proceso'
            reporte.save(update_fields=['asignado_a', 'estado'])
        else:
            reporte.save(update_fields=['asignado_a'])

        asignado_nombre = f"{getattr(mantenedor, 'first_name', '')} {getattr(mantenedor, 'last_name', '')}".strip() or mantenedor.get_username()

    return JsonResponse({
        "ok": True,
        "reporte_id": reporte.pk,
        "asignado_nombre": asignado_nombre,
        "estado": reporte.get_estado_display(),
    })

@rol_requerido(["administracion"])
@login_required
def panel_admin(request):
    return render(request, "app/panel_admin.html")

@rol_requerido(["administracion"])
@login_required
def panel_admin_ubicacion(request):
    return render(request, "app/panel_admin_ubicacion.html")


# === Vistas de Listado protegidas por rol Administracion ===

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class CategoriaListView(ListView):
    model = Categoria
    paginate_by = 10
    template_name = "app/list_categoria.html"

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PrioridadListView(ListView):
    model = Prioridad
    paginate_by = 10
    template_name = "app/list_prioridad.html"

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class RolListView(ListView):
    model = Rol
    paginate_by = 10
    template_name = "app/list_rol.html"

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class GeneroListView(ListView):
    model = Genero
    paginate_by = 10
    template_name = "app/list_genero.html"

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class EdificioListView(ListView):
    model = Edificio
    paginate_by = 10
    template_name = "app/list_edificio.html"

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
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

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class SalaListView(ListView):
    model = Sala
    paginate_by = 10
    template_name = "app/list_sala.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("edificio", "piso", "piso__edificio")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(codigo__icontains=q) |
                Q(nombre__icontains=q) |
                Q(edificio__nombre__icontains=q) |
                Q(piso__etiqueta__icontains=q)
            )
        return qs


# === Create / Update / Delete protegidas también ===

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "app/form_categoria.html"
    success_url = reverse_lazy("categoria-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PrioridadCreateView(CreateView):
    model = Prioridad
    form_class = PrioridadForm
    template_name = "app/form_prioridad.html"
    success_url = reverse_lazy("prioridad-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class RolCreateView(CreateView):
    model = Rol
    form_class = RolForm
    template_name = "app/form_rol.html"
    success_url = reverse_lazy("rol-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class GeneroCreateView(CreateView):
    model = Genero
    form_class = GeneroForm
    template_name = "app/form_genero.html"
    success_url = reverse_lazy("genero-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class EdificioCreateView(CreateView):
    model = Edificio
    form_class = EdificioForm
    template_name = "app/form_edificio.html"
    success_url = reverse_lazy("edificio-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PisoCreateView(CreateView):
    model = Piso
    form_class = PisoForm
    template_name = "app/form_piso.html"
    success_url = reverse_lazy("piso-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class SalaCreateView(CreateView):
    model = Sala
    form_class = SalaForm
    template_name = "app/form_sala.html"
    success_url = reverse_lazy("sala-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "app/form_categoria.html"
    success_url = reverse_lazy("categoria-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PrioridadUpdateView(UpdateView):
    model = Prioridad
    form_class = PrioridadForm
    template_name = "app/form_prioridad.html"
    success_url = reverse_lazy("prioridad-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class RolUpdateView(UpdateView):
    model = Rol
    form_class = RolForm
    template_name = "app/form_rol.html"
    success_url = reverse_lazy("rol-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class GeneroUpdateView(UpdateView):
    model = Genero
    form_class = GeneroForm
    template_name = "app/form_genero.html"
    success_url = reverse_lazy("genero-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class EdificioUpdateView(UpdateView):
    model = Edificio
    form_class = EdificioForm
    template_name = "app/form_edificio.html"
    success_url = reverse_lazy("edificio-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PisoUpdateView(UpdateView):
    model = Piso
    form_class = PisoForm
    template_name = "app/form_piso.html"
    success_url = reverse_lazy("piso-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class SalaUpdateView(UpdateView):
    model = Sala
    form_class = SalaForm
    template_name = "app/form_sala.html"
    success_url = reverse_lazy("sala-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("categoria-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PrioridadDeleteView(DeleteView):
    model = Prioridad
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("prioridad-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class RolDeleteView(DeleteView):
    model = Rol
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("rol-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class GeneroDeleteView(DeleteView):
    model = Genero
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("genero-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class EdificioDeleteView(DeleteView):
    model = Edificio
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("edificio-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class PisoDeleteView(DeleteView):
    model = Piso
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("piso-list")

@method_decorator(rol_requerido(["administracion"]), name="dispatch")
@method_decorator(login_required, name="dispatch")
class SalaDeleteView(DeleteView):
    model = Sala
    template_name = "app/confirm_delete.html"
    success_url = reverse_lazy("sala-list")
