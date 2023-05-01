from django import forms

from .models import Usuario, Mascota_Adopcion

class UsuarioForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Usuario  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = '__all__'  #Todos los campos del modelo

class MascotaAdopcionForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Mascota_Adopcion  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = ['nombre','color', 'raza', 'fecha_nac']