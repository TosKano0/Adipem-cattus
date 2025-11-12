from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.exceptions import ValidationError

class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='reportes/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 👇 Campo obligatorio: quién creó el reporte
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reportes_creados'
    )

    # 👇 Estado del reporte
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    # 👇 Opcional: asignado a un usuario de mantenimiento
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reportes_asignados'
    )

    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_ultima_reasignacion = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original = type(self).objects.only('estado', 'asignado_a').get(pk=self.pk)
            if original.estado == 'completado':
                if (self.estado != original.estado) or (self.asignado_a_id != original.asignado_a_id):
                    raise ValidationError("Reporte completado: no se pueden modificar estado ni mantenedor.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class HistorialAsignacion(models.Model):
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE, related_name='historial_asignaciones')

    # antes y después (pueden ser NULL si no había asignación)
    asignado_de = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='historial_asignado_desde'
    )
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='historial_asignado_hacia'
    )

    # opcional: también guarda cambios de estado si ocurren en la misma operación
    estado_de = models.CharField(max_length=20, blank=True, null=True)
    estado_a = models.CharField(max_length=20, blank=True, null=True)

    # quién ejecutó el cambio
    cambiado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='historial_cambios_asignacion'
    )

    # por si quieres anotar un motivo/comentario
    motivo = models.CharField(max_length=255, blank=True)

    # cuándo ocurrió
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['reporte', 'creado_en']),
            models.Index(fields=['asignado_a']),
        ]

    def __str__(self):
        de = self.asignado_de.username if self.asignado_de else "Sin asignación"
        a = self.asignado_a.username if self.asignado_a else "Sin asignación"
        return f"[{self.creado_en:%Y-%m-%d %H:%M}] {self.reporte_id}: {de} → {a}"

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un username")
        email = self.normalize_email(email)
        extra_fields.setdefault("nombre_rol", extra_fields.get("nombre_rol") or "usuario")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("nombre_rol", "administracion")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    GENERO_CHOICES = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro"),
    ]
    ROL_CHOICES = [
        ("usuario", "Usuario"),
        ("administracion", "Administración"),
        ("mantenimiento", "Mantenimiento"),
    ]

    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=12, choices=GENERO_CHOICES, blank=True)
    nombre_rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="usuario")

    email = models.EmailField(unique=True)

    objects = UsuarioManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Prioridad(models.Model):
    nivel = models.CharField(max_length=100)

    def __str__(self):
        return self.nivel

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Genero(models.Model):
    genero = models.CharField(max_length=100)

    def __str__(self):
        return self.genero

class Edificio(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    codigo = models.SlugField(max_length=32, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Piso(models.Model):
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="pisos")
    numero = models.IntegerField(
        validators=[MinValueValidator(-5), MaxValueValidator(200)]
    )
    etiqueta = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["edificio", "numero"]
        constraints = [
            models.UniqueConstraint(fields=["edificio", "numero"], name="piso_unico_por_edificio"),
        ]

    def __str__(self):
        return f"Piso {self.numero} — {self.edificio.codigo.upper()}"

class Sala(models.Model):
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="salas")
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, related_name="salas")
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["edificio", "piso__numero", "codigo"]
        constraints = [
            models.UniqueConstraint(fields=["edificio", "codigo"], name="codigo_sala_unico_por_edificio"),
        ]

    def save(self, *args, **kwargs):
        if self.piso_id:
            self.edificio = self.piso.edificio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} — {self.edificio.codigo.upper()} (Piso {self.piso.numero})"
