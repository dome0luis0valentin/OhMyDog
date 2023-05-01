from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

#https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Models

# Create your models here.

#ACA FALTAN TODOS LO MODELOS DE LAS BASE DE DATOS

#Este modelo lo uso para el FormModel
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=200,)
    correo = models.EmailField( unique=True)
    telefono = models.CharField(max_length=20)
    mascotas = models.ManyToManyField('Mascota', blank=True)    
    mascotas_adopcion = models.ManyToManyField('Mascota_Adopcion', blank=True)


    def __str__(self) -> str:
        return self.apellido
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('usuario-detalle', args=[str(self.id)])
    
class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    dueno = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    nombre = models.CharField(max_length= 100)
    color = models.CharField(max_length=50)
    raza = models.CharField(max_length=1000)
    fecha_nac = models.DateField()
    foto = models.FileField(blank=True)

    def __str__(self) -> str:
        return self.nombre
    
class Mascota_Adopcion(models.Model):
    id = models.AutoField(primary_key=True)
    dueno = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    nombre = models.CharField(max_length= 100)
    color = models.CharField(max_length=50)
    raza = models.CharField(max_length=1000)
    fecha_nac = models.DateField()
    ESTADO_ADOPCION = (
        ('a', 'Adoptado'),
        ('e', 'Esperando'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_ADOPCION, blank=True, default='e', help_text='Estado del perro')

    def __str__(self) -> str:
        return self.nombre
    
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular del modelo.
        """
        return "http://127.0.0.1:8000/adopcion/"+str(self.id)
    
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario =models.CharField(max_length=50)
    password = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.nombre_usuario

class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    fecha= models.DateTimeField()
    asistio = models.BooleanField()
    motivo= models.CharField(max_length=50)
    aceptado= models.BooleanField()
    turnos= models.ForeignKey(Cliente,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.fecha

class Campana(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    motivo = models.CharField(max_length=50)
    fecha_fin=models.DateTimeField()
    Total_donado =models.FloatField()

    def __str__(self) -> str:
        return self.nombre
            