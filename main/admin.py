from django.contrib import admin
from .models import Mascota ,Persona, Cliente, Campana, Turno, Mascota_Adopcion, Red_Social, Prestador_Servicios
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Turno)
admin.site.register(Campana)
admin.site.register(Mascota)
admin.site.register(Mascota_Adopcion)
admin.site.register(Prestador_Servicios)
admin.site.register(Persona)
admin.site.register(Red_Social)

