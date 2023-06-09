from django.urls import path 
from . import views

urlpatterns = [
    path('solicitar_turno/', views.solicitar_turno, name='solicitar turno'),
    path('confirmar_turnos/', views.TurnosListView.as_view(), name='confirmar_turnos'),
    path('confirmar_turnos/<int:pk>', views.turno_detail_view, name='detalle de turno'),
    path('aceptar_turno/<int:turno_id>', views.aceptar_turno, name='aceptar turno'),
    path('rechazar_turno/<int:turno_id>', views.rechazar_turno, name='rechazar turno'),
    path('turnos_programados/', views.turnos_programados , name='turnos_programados'),
    path('turnos_confirmadosHasta/', views.turnos_solo_confirmados , name='turnos_confirmados'),
    path('turnos_confirmados/<int:pk>/<str:tipo>', views.turno_confirmado_detail_view , name='detalle de turno confirmado'),
    path('Asistio_al_turno/<int:turno_id>', views.Asistio_al_turno, name='Asistio_al_turno'),
    path('Falto_al_turno/<int:turno_id>', views.Falto_al_turno, name='Falto_al_turno'),
    
    #Veterinarias de turno
    
    path('cargar_veterinarias/',views.cargar_veterinarias, name="cargar veterinarias de turno"),
    path('ver_veterinarias_de_turno/',views.ver_veterinarias_de_turno, name="ver veterinarias de turno"),
    path('confirmar_borrar_veterinarias_de_turno/',views.confirmar_borrar_veterinarias_de_turno, name="confirmar borrar veterinarias de turno"),
    path('borrar_veterinarias_de_turno/',views.borrar_veterinarias_de_turno, name="borrar veterinarias de turno"),
    
    
    path('ver_historial_de_turnos/',views.ver_historial_de_turnos, name="ver historial de turnos"),
    path('formulario_simple/<int:turno_id>/',views.formulario_simple, name="formulario_simple"),
    path('formulario_desparasitante/<int:turno_id>/',views.formulario_desparasitante, name="formulario_desparasitante"),
    path('formulario_vacunacion/<int:turno_id>/',views.formulario_vacunacion, name="formulario_vacunacion"),
    path('actualizar_turno/<int:turno_id>/<str:monto>/', views.actualizar_turno, name='actualizar_turno'),
    path('calcelar_turno/<int:turno_id>/', views.calcelar_turno, name='calcelar_turno'),
    path('ver_historial_de_visitas/<int:pk>',views.ver_historial_de_visitas, name="ver historial de visitas"),
    path('ver_todas_las_visitas/',views.ver_todas_las_visitas, name="ver todas las visitas"),
    path('detalle_visita/<int:id>',views.detalle_visita, name="detalle visita"),

    #Cobro
    path('ver_cobros/', views.ver_cobros, name="Ver cobros"),

    

    path('ver_libreta_sanitaria/<int:pk>',views.ver_libreta_sanitaria, name="ver libreta sanitaria"),



]
