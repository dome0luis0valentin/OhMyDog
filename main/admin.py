from django.contrib import admin
from .models import Usuario
from .models import Mascota, Cliente, Campana, Turno, Mascota_Adopcion
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Turno)
admin.site.register(Campana)
admin.site.register(Usuario)
admin.site.register(Mascota)
admin.site.register(Mascota_Adopcion)
