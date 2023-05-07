from django import forms

from .models import Cliente, Persona, Red_Social, Mascota_Adopcion, Mascota, Turno, Prestador_Servicios

from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Cliente  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = '__all__'  #Todos los campos del modelo

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ('nombre', 'color', 'raza', 'fecha_nac', 'foto')

    def __init__(self, *args, **kwargs):
        super(MascotaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['color'].required = True
        self.fields['raza'].required = True
        self.fields['fecha_nac'].required = True
        self.fields['foto'].required = False
class Red_SocialForm(forms.ModelForm):
    
    class Meta:
        model = Red_Social
        fields = ['usuario','nombre']

class ServicioForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50) 
    apellido = forms.CharField(max_length=50)
    dni = forms.IntegerField()
    direccion = forms.CharField(max_length=200,)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    red = Red_SocialForm

    class Meta:
        model = Prestador_Servicios
        fields = ['tipo']

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ('fecha', 'banda_horaria', 'motivo')

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].required = True
        self.fields['banda_horaria'].required = True
        self.fields['motivo'].required = True
        


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

