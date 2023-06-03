from django.db import models

# Create your models here.
class Visitas(models.Model):
    perdidacol VARCHAR(45)
    fecha DATETIME
    cliente_id INT
    cliente_persona_id_persona INT
    ultimo_lugar VARCHAR(100)
    otros VARCHAR(200)
    rasgos_particulares VARCHAR(100)
    descripcion VARCHAR(200)
    url_foto VARCHAR(150)
    encontrado TINYINT