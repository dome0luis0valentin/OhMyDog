from django.db import models
from main.models import Cliente, Mascota

# Create your models here.
class MascotasPerdidas(models.Model):
    nombre  = models.CharField(max_length=100, null=True)
    raza    = models.CharField(max_length=100, null=True)
    contacto= models.CharField(max_length=100, null=True)
    fecha   = models.DateField(null= True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    ultimo_lugar = models.CharField(max_length=100)
    rasgos_particulares = models.CharField(max_length=200, blank=True)
    descripcion = models.CharField(max_length=300)
    foto = models.ImageField(blank=True, upload_to="mascotas_perdidas/")
    encontrado = models.BooleanField(default=False, blank=True)

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/ver_perdidos/"+str(self.id)