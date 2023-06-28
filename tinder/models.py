from django.db import models
from main.models import Mascota
from main.models import Cliente

# Create your models here.
class UsuarioTinder(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete = models.PROTECT)
    dueno = models.ForeignKey(Cliente, on_delete = models.PROTECT)
    hembra = models.BooleanField()
    fecha_de_celo = models.CharField(max_length = 100, blank = True)
    contacto = models.CharField(max_length = 100)