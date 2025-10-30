# app/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='reportes/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo
class RegistroUsuario(models.Model):
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

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  #  reemplazar por hash si luego ocupamos (auth)
    edad = models.PositiveSmallIntegerField()
    genero = models.CharField(max_length=12, choices=GENERO_CHOICES)
    nombre_rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

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
    nombre = models.CharField(max_length=120, unique=True)          # "Edificio H"
    codigo = models.SlugField(max_length=32, unique=True)           # "h"

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Piso(models.Model):
    """
    Un piso pertenece a UN edificio. El 'number' puede repetirse entre edificios.
    Ej: number=2 en Edificio H y number=2 en Edificio A son filas distintas.
    """
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="pisos")
    numero = models.IntegerField(
        help_text="Usa negativos para subterráneos (−1, −2), 0 para zócalo si aplica, 1..N para niveles.",
        validators=[MinValueValidator(-5), MaxValueValidator(200)]
    )
    etiqueta = models.CharField(
        max_length=40, blank=True,
        help_text="Opcional: etiqueta visible (p. ej., 'Subterráneo 1', '2° Piso')"
    )

    class Meta:
        ordering = ["edificio", "numero"]
        constraints = [
            # Un número de piso sólo debe ser único dentro del MISMO edificio
            models.UniqueConstraint(fields=["edificio", "numero"], name="piso_unico_por_edificio"),
        ]

    def __str__(self):
        return f"Piso { self.numero} — {self.edificio.codigo.upper()}"

class Sala(models.Model):
    """
    Sala atada al piso. Guardamos 'edificio' denormalizado para filtros rápidos en admin.
    """
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="salas")
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, related_name="salas")
    codigo = models.CharField(max_length=50, help_text="Ej: H-201, H-203B")
    nombre = models.CharField(max_length=120, blank=True, help_text="Nombre legible: 'Laboratorio Redes'")

    class Meta:
        ordering = ["edificio", "piso__numero", "codigo"]
        constraints = [
            # Evita duplicar códigos de sala dentro del MISMO edificio
            models.UniqueConstraint(fields=["edificio", "codigo"], name="codigo_sala_unico_por_edificio"),
        ]

    def save(self, *args, **kwargs):
        # Mantén building consistente con floor.building
        if self.piso_id:
            self.edificio = self.piso.edificio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} — {self.edificio.codigo.upper()} (Piso {self.piso.numero})"