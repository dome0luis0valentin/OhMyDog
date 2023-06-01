from django.db import models

class Veterinarias_de_turno(models.Model):
    arch= models.FileField(blank=True, upload_to="archivos/")
    
    fecha_creación = models.DateField(blank=True)

    def __str__(self) -> str:
        return self.fecha_creación