from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

#from django.contrib.auth.models import User
#Usuario nuevo

from django.contrib.auth.models import AbstractUser

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

#https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Models

# Create your models here.

#ACA FALTAN TODOS LO MODELOS DE LAS BASE DE DATOS

class User(AbstractUser):
    is_veterinario = models.BooleanField(null=True, default=False)
    descuento = models.IntegerField(default=0, blank=True)

class Persona(models.Model):
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
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
    foto = models.ImageField(blank=True, upload_to='imagenes/', error_messages={
            'invalid': 'El archivo debe ser una imagen'
        })
    perdida = models.BooleanField(default=False, blank=True)
    viva = models.BooleanField(default=True, blank=True, null = True)

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
    fecha= models.DateField(error_messages={
            'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD'
        })
    asistio = models.BooleanField()
    cliente= models.ForeignKey(Cliente,on_delete=models.CASCADE)

    ESTADO = (
        ('E','Esperando Confirmacion'),
        ('A','Aceptado'),
        ('R','Rechazado'),
        ('As', 'Asistio'),
        ('Ca', 'Cancelado'),
        ('F', 'Falto')
    )

    MOTIVO = (
        ('Consulta','Consulta'),
        ('Urgencia','Urgencia'),
        ('Castración','Castración'),
        ('Vacunación de tipo A','Vacunación de tipo A'),
        ('Vacunación de tipo B','Vacunación de tipo B'),
        ('Desparasitación','Desparasitación')
    )
    BANDA_HORARIA = (
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
    )

    banda_horaria = models.CharField(max_length=100, choices=BANDA_HORARIA, default='Mañana', help_text='Mañana(7 a 12hs) - Tarde(12 a 18hs)')
    motivo= models.CharField(max_length=100, choices=MOTIVO, default='Consulta')
    estado = models.CharField(max_length=100, choices=ESTADO, blank=True, default='Esperando Confirmación')
   
    mascota = models.ForeignKey(Mascota, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.fecha.day)+"/"+str(self.fecha.month)
    
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular del modelo.
        """
        return "http://127.0.0.1:8000/confirmar_turnos/"+str(self.id)
      
class Vacuna_tipoA(models.Model):
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha_aplicacion = models.DateField()
    
class Vacuna_tipoB(models.Model):
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha_aplicacion = models.DateField()    

class Campana(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    motivo = models.CharField(max_length=50)
    fecha_fin=models.DateField(error_messages={
            'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD'
        })
    Total_donado =models.FloatField()

            

class Prestador_Servicios(models.Model):
    datos = models.ForeignKey(Persona, on_delete=models.CASCADE)
    zona = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(25)], blank= True, default=1)

    def __str__(self) -> str:
        return self.datos.nombre
    
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular del modelo.
        """
        return "http://127.0.0.1:8000/ver_servicios/"+str(self.id)
    
    TIPO_SERVICIO = (
        ('p', 'Paseador'),
        ('c', 'Cuidador'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_SERVICIO,  default='p', help_text='Tipo de servicio que presta la persona')

class Red_Social(models.Model):
    nombre_red = models.CharField(max_length=50)
    usuario_red = models.CharField(max_length=70)
    dueno = models.ForeignKey(Prestador_Servicios, on_delete=models.PROTECT)

class Intentos(models.Model):
    usuario = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=0)
    ESTADO_USUARIO = (
        ('b', 'bloqueado'),
        ('n', 'no bloqueado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_USUARIO, default='n')

class Visitas(models.Model):
    #Datos del turno
    fecha   = models.DateField(null=True)
    motivo  = models.CharField(max_length=45, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.PROTECT , null=True)

    #Datos comunes
    observaciones= models.CharField(max_length=500, null=True)
    monto = models.DecimalField(max_digits=60, decimal_places=30, null=True)
    
    #Particulares Opcionales de Vacu. o Desp.
    peso    = models.DecimalField(max_digits=6, decimal_places=3,null=True, blank=True)
    codigo  = models.CharField(max_length=20, blank=True)
    cant_desparacitante= models.DecimalField(max_digits=6, decimal_places=3,null=True, blank=True)
    