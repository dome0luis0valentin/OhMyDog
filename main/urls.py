from django.urls import path
from . import views

#Estos van a ser las secciones  de la pagina

urlpatterns = [
    path('menu_principal/', views.main, name="menu"),
    path('about/', views.about, name="about"),
    path('lista_mascotas/', views.lista_mascotas, name="lista_mascotas"),
]