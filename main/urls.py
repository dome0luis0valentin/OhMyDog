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
    path('lista_mascota/', views.lista_mascota, name="lista_mascota"),
    path('mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mascota'),

    path('detalle_mascota_view/<int:id>',views.detalle_mascota, name="detalle_mascota_view"),
    path('adopcion/<int:pk>', views.AdopcionDetailView.as_view(), name='detalle de mascota'),
    path('adopcion/', views.AdopcionListView.as_view(), name='adopciones'),

    path('registrar_adopcion/', views.registrar_adopcion, name='registrar adopcion'),

    path('ver_mis_mascotas/', views.MascotaListView.as_view(), name='Ver mis Mascotas'),
    path('ver_mis_mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mis mascota'),
    
]
