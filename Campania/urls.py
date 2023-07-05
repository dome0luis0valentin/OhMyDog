from django.urls import path 
from . import views

urlpatterns = [
    path('crear_campana/', views.crear_campana , name='crear_campana'),
    path('formulario_pago/<int:campana_id>/<int:user_id>', views.formulario_pago , name='formulario_pago'),
    path('formulario_pago_visitante/<int:campana_id>/', views.formulario_pago_visitante , name='formulario_pago_visitante'),
    path('ver_campanas/<int:user_id>/', views.ver_campanas, name='ver_campanas'),
    path('ver_campanas/', views.ver_campanas_visitante, name='ver_campanas'),
    path('ver_mis_donaciones/', views.ver_mis_donaciones, name = 'ver mis donaciones'),
    #Donaciones
    path('ver_donacionesa_a_campaña/<int:pk>/', views.ver_donacionesa_a_campaña, name="Ver donaciones a campaña"),
    path('ver_donaciones/', views.ver_donaciones, name="Ver donaciones"),

]