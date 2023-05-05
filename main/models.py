from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Models

# Create your models here.

#ACA FALTAN TODOS LO MODELOS DE LAS BASE DE DATOS

#Este modelo lo uso para el FormModel
class Persona(models.Model):
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=200,)
    correo = models.EmailField( unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.apellido
    
class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    datos = models.ForeignKey(Persona, on_delete=models.PROTECT)
    mascotas = models.ManyToManyField('Mascota', blank=True)    
    mascotas_adopcion = models.ManyToManyField('Mascota_Adopcion', blank=True)
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.usuario.first_name

class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    dueno = models.ForeignKey('Cliente', on_delete = models.PROTECT)
    nombre = models.CharField(max_length= 100)
    color = models.CharField(max_length=50)
    raza = models.CharField(max_length=1000)
    fecha_nac = models.DateField()
    foto = models.FileField(blank=True, upload_to='imaganes/')

    def __str__(self) -> str:
        return self.nombre
    
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular del modelo.
        """
        return "http://127.0.0.1:8000/ver_mis_mascotas/"+str(self.id)
    
class Mascota_Adopcion(models.Model):
    id = models.AutoField(primary_key=True)
    dueno = models.ForeignKey('Cliente', on_delete = models.PROTECT)
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
    
    @property
    def is_adoptado(self):
        if self.estado == 'a':
            return True
        return False

class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    fecha= models.DateTimeField()
    asistio = models.BooleanField()
    motivo= models.CharField(max_length=50)
    aceptado= models.BooleanField()
    cliente= models.ForeignKey(Cliente,on_delete=models.CASCADE)

    BANDA_HORARIA = (
        ('M', 'Mañana'),
        ('T', 'Tarde'),
    )

    banda_horaria = models.CharField(max_length=1, choices=BANDA_HORARIA, default='M', help_text='Horario en el que puede ir a la veterinaria mañana(7 AM - 12 PM) o tarde (12 PM a 6 PM')


    def __str__(self) -> str:
        return str(self.fecha.day)+"/"+str(self.fecha.month)
    
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular del modelo.
        """
        return "http://127.0.0.1:8000/confirmar_turnos/"+str(self.id)

class Campana(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    motivo = models.CharField(max_length=50)
    fecha_fin=models.DateTimeField()
    Total_donado =models.FloatField()

    def __str__(self) -> str:
        return self.nombre
            

class Prestador_Servicios(models.Model):
    datos = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.datos.nombre
    
    TIPO_SERVICIO = (
        ('p', 'Paseador'),
        ('c', 'Cuidador'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_SERVICIO,  default='p', help_text='Tipo de servicio que presta la persona')

class Red_Social(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.CharField(max_length=70)
    dueno = models.ForeignKey(Prestador_Servicios, on_delete=models.PROTECT)
