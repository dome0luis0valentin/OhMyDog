from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

#https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Models

# Create your models here.

#ACA FALTAN TODOS LO MODELOS DE LAS BASE DE DATOS

#Este modelo lo uso para el FormModel
class Usuario(models.Model):
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=200,)
    correo = models.EmailField( unique=True)
    telefono = models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.apellido
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('usuario-detalle', args=[str(self.id)])
    
class Mascota(models.Model):
    dueño = models.ForeignKey(Usuario, on_delete = models.PROTECT, default = None, related_name="dueño" )
    nombre = models.CharField(max_length= 100)
    color = models.CharField(max_length=50)
    raza = models.CharField(max_length=1000)
    fecha_nac = models.DateField()
    foto = models.FileField()

    def __str__(self) -> str:
        return self.nombre
    
class Mascota_Adopcion(models.Model):
    datos = models.ForeignKey(Mascota,on_delete = models.PROTECT, default = None, related_name="datos_mascota")
