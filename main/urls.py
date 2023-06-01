from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from OhMyDog import settings
from django.conf.urls.static import static
#Estos van a ser las secciones  de la pagina


urlpatterns = [
    
    path('', views.main, name="main"),
    path('registro/', views.registro, name='registro'),
    path('registrar_primera_mascota/<str:email_de_cliente>', views.registrar_primera_mascota, name='registrar_primera_mascota'),
    path('confirmar_cerrar_sesion/', views.confirmar_cerrar_sesion, name='confirmar_cerrar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio de sesion'),
    path('usuario_bloqueado/', views.usuario_bloqueado, name='usuario bloqueado'),
    
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('confirmar_cambiar_contraseña/', views.confirmar_cambiar_contraseña, name='confirmar_cambiar_contraseña'),


    path('menu_principal/', views.main, name="menu"),
    path('about/', views.about, name="about"),

    path('registrar_mascota/', views.registrar_mascota, name='registrar mascota'),
    path('lista_mascota/', views.MascotaDetailView.as_view(), name="lista mascota"),
    path('mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mascota'),
    path('detalle_mascota_view/<int:id>',views.detalle_mascota, name="detalle_mascota_view"),
    path('ver_mis_mascotas/', views.MascotaListView.as_view(), name='Ver mis Mascotas'),
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('confirmar_eliminar_mascota/<int:mascota_id>/', views.confirmar_eliminar_mascota, name='confirmar_eliminar_mascota'),
    path('ver_mis_mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mis mascota'),

    path('adopcion/<int:pk>', views.AdopcionDetailView.as_view(), name='detalle de mascota'),
    path('adopcion/', views.AdopcionListView.as_view(), name='adopciones'),
    path('ver_mis_adopciones/', views.MisAdopcionesListView.as_view(), name='ver mis adopciones'),
    path('formulario_adopcion/', views.enviar_formulario_adopcion, name='enviar_formulario_adopcion'),
    path('marcar_adopcion/<int:pk>/', views.marcar_adopcion, name='marcar_adopcion'),
    path('registrar_adopcion/', views.registrar_adopcion, name='registrar adopcion'),    
    
    path('registrar_servicio/', views.registrar_servicio, name='registrar servicio'),
    path('ver_servicios/', views.ServiciosListView.as_view(), name='ver servicio'),
    path('ver_servicios/<int:pk>',views.servicio_detail_view, name="detalle servicio"), 
    path('favicon.ico', RedirectView.as_view(url='/main/static/img/favicon.ico')),

    #path('registrar_urgencia/', views.registrar_urgencia, name = 'registrar urgencia'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

