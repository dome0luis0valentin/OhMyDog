from django.db import models

# Create your models here.

#Este modelo lo uso para el FormModel
class Usuario(models.Model):
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.apellido
    
class Mascota(models.Model):
    nombre = models.CharField(max_length= 100)
    color = models.FloatField()
    raza = models.CharField(max_length=1000)
    fecha_nac = models.DateTimeField()
    foto = models.FileField()

    def __str__(self) -> str:
        return self.nombre