# app/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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

    def __str__(self):
        return self.titulo


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

    # Campos adicionales
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=12, choices=GENERO_CHOICES, blank=True)
    nombre_rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="usuario")

    # 👇 Asegurar que el email sea único y obligatorio
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modelos auxiliares (sin cambios)
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