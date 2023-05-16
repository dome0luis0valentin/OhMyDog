from django import forms

from django.core.validators import FileExtensionValidator

from .models import Cliente, Persona, Red_Social, Mascota_Adopcion, Mascota, Turno, Prestador_Servicios

from django.contrib.auth.forms import UserCreationForm


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image(file):
    if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
        raise ValidationError(
            _('El archivo subido no es una imagen válida.')
        )
    

class UsuarioForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Cliente  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = '__all__'  #Todos los campos del modelo

class MascotaForm(forms.ModelForm):

    fecha_nac = forms.DateField(error_messages={
        'invalid': 'El formato de fecha es inválido. Use el formato AAAA-MM-DD.'
    })
    foto = forms.ImageField(validators=[validate_image])

    class Meta:
        model = Mascota
        fields = ('nombre', 'color', 'raza')

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
        fields = ['usuario_red','nombre_red']

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

class UrgenciaForm(forms.ModelForm):
    cliente = forms.EmailField(max_length=70)
    turno = TurnoForm
    fecha = forms.DateField(
        error_messages={
            'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD.'
        }
    )
    
    class Meta:
        model = Turno
        fields = ('fecha', 'banda_horaria', 'motivo')

    def __init__(self, *args, **kwargs):
        super(UrgenciaForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].required = True
        self.fields['banda_horaria'].required = True
        self.fields['motivo'].required = True
        
class MascotaAdopcionForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Mascota_Adopcion  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = ['nombre','color', 'raza', 'fecha_nac']


