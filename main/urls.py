from django.urls import path, include



from . import views

#Estos van a ser las secciones  de la pagina


urlpatterns = [
    
    path('', views.main, name="main"),
    path('inisio_Sesion/', views.inisio_Sesion, name="inisio_Sesion"),
    path('menu_principal/', views.main, name="menu"),
    path('about/', views.about, name="about"),
    path('lista_mascota/', views.lista_mascota, name="lista_mascota"),
    path('registrar/', views.registro, name="registar"),
    path('detalle_mascota/', views.detalle_mascota, name="ver detalle mascota"),

    path('detalle_mascota_view/<int:id>',views.detalle_mascota, name="detalle_mascota_view"),
    path('adopcion/<int:pk>', views.AdopcionDetailView.as_view(), name='detalle de mascota'),
    path('adopcion/', views.AdopcionListView.as_view(), name='adopciones'),

    path('registrar_adopcion/', views.registrar_adopcion, name='registrar adopcion'),

    path('ver_mis_mascotas/', views.MascotaListView.as_view(), name='Ver mis Mascotas'),
    path('ver_mis_mascotas/<int:pk>', views.MascotaDetailView.as_view(), name='detalle de mis mascota'),
    
]

