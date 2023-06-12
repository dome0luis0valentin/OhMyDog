from django import forms

from django.core.validators import FileExtensionValidator

from .models import Cliente, Persona, Red_Social, Mascota_Adopcion, Mascota, Turno, Prestador_Servicios

from django.contrib.auth.forms import UserCreationForm

from django import forms


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _


def validate_image(file):
    if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
        raise ValidationError(
            _('El archivo subido no es una imagen válida.')
        )
    

class FormularioAdopcionForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=100)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=100)
    motivo = forms.CharField(widget=forms.Textarea)


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': _("Las contraseñas no coinciden."),
        'password_incorrect': _("La contraseña actual es incorrecta."),
        'password_entirely_numeric': _("La contraseña no puede ser completamente numérica."),
    }

    help_texts = {
        'password_current': _("Ingrese su contraseña actual."),
        'password_new': _("Ingrese una nueva contraseña."),
        'password_new_confirm': _("Confirme su nueva contraseña."),
    }



class UsuarioForm(forms.ModelForm):

    #Para validar los datos en el formulario falta implementar esto:

    #https://runebook.dev/es/docs/django/ref/forms/validation
    
    class Meta: 
        model = Cliente  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = '__all__'  #Todos los campos del modelo


class MascotaForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Nombre'})) 
    color = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Color'})) 
    raza = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Raza'})) 
   
    
    fecha_nac = forms.DateField(error_messages={
        'invalid': 'El formato de fecha es inválido. Use el formato AAAA-MM-DD.'
    })
    fecha_nac = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))

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
    nombre = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Nombre'})) 
    apellido = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Apellido'}))
    dni = forms.IntegerField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese DNI'}))
    direccion = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Direccion '}))
    correo = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'class': 'col-5','placeholder':'ejemplo@gmail.com'}))
    telefono = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Telefono'}))
    red = Red_SocialForm

    class Meta:
        model = Prestador_Servicios
        fields = ['tipo', 'zona']

class TurnoForm(forms.ModelForm):
    
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.none())
    fecha = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))
    class Meta:
        model = Turno
        fields = ('fecha', 'banda_horaria', 'motivo', 'mascota')

    def __init__(self, dueño_cliente, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].required = True
        self.fields['banda_horaria'].required = True
        self.fields['motivo'].required = True
        self.fields['mascota'].queryset = Mascota.objects.filter(dueno_id = dueño_cliente)

class UrgenciaForm(forms.ModelForm):
    cliente = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'class': 'col-5','placeholder':'ejemplo@gmail.com'}))
    turno = TurnoForm
    fecha = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))

    
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

    nombre = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Nombre'}))
    color = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Color'}))
    raza = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'col-5','placeholder':'Ingrese Raza'}))
    fecha_nac = forms.DateField(widget=forms.widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'col-5'}))
    
    class Meta: 
        model = Mascota_Adopcion  #Busco el modelo, para cada campo del modelo, hará una entrada al formularion
        fields = ['nombre','color', 'raza', 'fecha_nac']