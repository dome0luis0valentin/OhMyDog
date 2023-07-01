from django.db import models
from main.models import Cliente, Mascota

class Veterinarias_de_turno(models.Model):
    arch= models.FileField(blank=True, upload_to="archivos/")
    
    fecha_creación = models.DateField(blank=True)

    def __str__(self) -> str:
        return self.fecha_creación
    
class Cobro(models.Model):
   monto    = models.DecimalField(max_digits=10, decimal_places=2, null=True)
   descuento= models.DecimalField(max_digits=10, decimal_places=2, null=True)
   cliente  = models.CharField(max_length=200)
   fecha    = models.DateField()
   mascota  = models.CharField(max_length=200)
   motivo   = models.CharField(max_length=100)