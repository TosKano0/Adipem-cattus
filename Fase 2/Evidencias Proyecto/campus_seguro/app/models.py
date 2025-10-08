# app/models.py
from django.db import models

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
