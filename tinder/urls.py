from . import views
from django.urls import path, include


urlpatterns = [  
    path("registrar_mascota_tinder/", views.registrar, name = "registrar"), 
    path("ver_mis_mascotas_tinder/", views.ver_mis_mascotas, name = "ver mis mascotas tinder"), 
    path("ver_mascotas_tinder/", views.ver_mascotas, name = "ver mascotas tinder"), 
    path("dar_de_baja_mascota_tinder/", views.dar_de_baja, name = "dar de baja mascota tinder"), 
]