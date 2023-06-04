from django.db import models
from main.models import Cliente

# Create your models here.

class MascotasEncontradas(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True)
    contacto= models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=300) 
    foto = models.ImageField(blank=True, upload_to="mascotas_encontradas/")
    devuelto = models.BooleanField(default=False, blank=True)

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/ver_encontrados/"+str(self.id)