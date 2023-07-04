from . import views
from django.urls import path, include


urlpatterns = [  
    path("publicar/", views.publicar, name = "publicar"),
    path("publicar_no_registrada/", views.publicar_no_registrada, name = "publicar no registrada"),
    path("ver_perdidos/", views.ver_perdidos, name = "ver perididos"),
    path("ver_perdidosSinAuth/", views.ver_perdidos, name = "ver perididos"),
    path("ver_perdidos/<int:pk>", views.PerdidosDetailView.as_view(), name = "ver detalle perididos"),
    path("ver_mis_perdidos/", views.ver_mis_perdidos, name = "ver mis perididos"),
    path("marcar_encontrado/<int:pk>", views.marcar_encontrado, name = "marcar encontrado"),
    
]