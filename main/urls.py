from django.urls import path, include



from . import views

#Estos van a ser las secciones  de la pagina


urlpatterns = [
    
    path('', views.main, name="main"),
    path('registro/', views.registro, name='registro'),
    path('cerrar_sesion/', views.cerrar_sesion, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio de sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar contraseña'),


    path('menu_principal/', views.main, name="menu"),
    path('about/', views.about, name="about"),

    path('registrar_mascota/', views.registrar_mascota, name='registrar mascota'),
    path('lista_mascota/', views.MascotaDetailView.as_view(), name="lista mascota"),
    path('mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mascota'),
    path('detalle_mascota_view/<int:id>',views.detalle_mascota, name="detalle_mascota_view"),
    path('ver_mis_mascotas/', views.MascotaListView.as_view(), name='Ver mis Mascotas'),
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('ver_mis_mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mis mascota'),

    path('adopcion/<int:pk>', views.AdopcionDetailView.as_view(), name='detalle de mascota'),
    path('adopcion/', views.AdopcionListView.as_view(), name='adopciones'),
    path('ver_mis_adopciones/', views.MisAdopcionesListView.as_view(), name='ver mis adopciones'),
    path('formulario_adopcion/', views.enviar_formulario_adopcion, name='enviar_formulario_adopcion'),
    path('marcar_adopcion/<int:pk>/', views.marcar_adopcion, name='marcar_adopcion'),
    path('registrar_adopcion/', views.registrar_adopcion, name='registrar adopcion'),

    path('solicitar_turno/', views.solicitar_turno, name='solicitar turno'),
    path('confirmar_turnos/', views.TurnosListView.as_view(), name='confirmar turnos'),
    path('confirmar_turnos/<int:pk>', views.TurnoDetailView.as_view(), name='detalle de turno'),

    path('registrar_servicio/', views.registrar_servicio, name='registrar servicio'),
    path('ver_servicios/', views.ServiciosListView.as_view(), name='ver servicio'),
    path('ver_servicios/<int:pk>',views.ServicioDetailView.as_view(), name="detalle servicio"),
    
    
]
