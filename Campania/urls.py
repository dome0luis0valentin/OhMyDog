from django.urls import path 
from . import views

urlpatterns = [
    path('crear_campana/', views.crear_campana , name='crear_campana'),
    #path('formulario_pago/<str:campana.id>', views.crear_campana , name='formulario_pago'),
    path('ver_campanas/', views.ver_campanas, name='ver_campanas')
]