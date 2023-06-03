from django.urls import path 
from . import views

urlpatterns = [
    path('crear_campana/', views.crear_campana , name='crear_campana')
]