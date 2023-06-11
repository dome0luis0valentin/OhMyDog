from django.db import models
from django.db import models
from main.models import User

class Donaciones(models.Model):
    campania = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Donacion de {self.usuario} a la campaña {self.campania}"

