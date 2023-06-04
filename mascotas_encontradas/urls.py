from . import views
from django.urls import path, include


urlpatterns = [  
    path("publicar_encontrada/", views.publicar, name = "publicar encontrada"),
    path("ver_encontrados/", views.ver_encontrados, name = "ver encontrados"),
    path("ver_encontrados/<int:pk>", views.EncontradosDetailView.as_view(), name = "ver detalle encontrados"),
    path("ver_mis_encontrados/", views.ver_mis_encontrados, name = "ver mis encontrados"),
    path("marcar_devuelto/<int:pk>", views.marcar_devuelto, name = "marcar devuelto"),
    
]