from django.urls import path 
from . import views

urlpatterns = [
    path('crear_campana/', views.crear_campana , name='crear_campana'),
    path('formulario_pago/<int:campana_id>/<int:user_id>', views.formulario_pago , name='formulario_pago'),
    path('ver_campanas/<int:user_id>/', views.ver_campanas, name='ver_campanas')
]