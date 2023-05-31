from django.urls import path 
from . import views

urlpatterns = [
    path('solicitar_turno/', views.solicitar_turno, name='solicitar turno'),
    path('confirmar_turnos/', views.TurnosListView.as_view(), name='confirmar_turnos'),
    path('confirmar_turnos/<int:pk>', views.turno_detail_view, name='detalle de turno'),
    path('aceptar_turno/<int:turno_id>', views.aceptar_turno, name='aceptar turno'),
    path('rechazar_turno/<int:turno_id>', views.rechazar_turno, name='rechazar turno'),
    path('turnos_confirmados/', views.turnos_confirmados , name='turnos confirmados'),
    path('detalle_mascota_view/<int:id>',views.detalle_mascota, name="detalle_mascota_view")

]
