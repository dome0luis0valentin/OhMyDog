from django import forms

from .models import Cliente, Persona, Mascota_Adopcion

from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Cliente  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = '__all__'  #Todos los campos del modelo


class MascotaAdopcionForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Mascota_Adopcion  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = ['nombre','color', 'raza', 'fecha_nac']


""" 
class RegistroForm(UserCreationForm):
    nombre_usuario = forms.CharField(max_length=50)
    correo = forms.EmailField(max_length=254)
    numero_telefono = forms.CharField(max_length=15)

    class Meta:
        model = Cliente
        fields = 
        #fields = ['nombre_usuario']
        #fields = '__all__'


class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    correo = forms.EmailField(max_length=254)
    telefono = forms.CharField(max_length=15)
    nombre_usuario = forms.CharField(max_length=30)
    direccion = forms.CharField(max_length= 100)
    dni =forms.IntegerField()

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellido', 'correo', 'telefono', 'nombre_usuario', 'password', 'direccion', 'dni')

    def save(self, commit=True):
        # Crear la instancia de Persona
        persona = Persona.objects.create(
            nombre=self.cleaned_data['nombre'],
            apellido=self.cleaned_data['apellido'],
            correo=self.cleaned_data['correo'],
            telefono=self.cleaned_data['telefono'],
            direccion = self.cleaned_data['direccion'],
            dni= self.cleaned_data['dni'],
        )
        # Crear la instancia de Cliente con la instancia de Persona relacionada
        cliente = Cliente.objects.create(
            datos=persona,
            nombre_usuario=self.cleaned_data['nombre_usuario'],
            password=self.cleaned_data['password']
        )
        # Crear la instancia de Usuario con la instancia de Cliente relacionada
        usuario = Cliente.objects.create(
            datos=persona,
            # otros campos de Usuario
        )
        return usuario

"""

