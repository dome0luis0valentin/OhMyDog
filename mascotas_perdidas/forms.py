from django import forms

from .models import MascotasPerdidas
from main.models import Mascota

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image(file):
    if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
        raise ValidationError(
            _('El archivo subido no es una imagen válida.')
        )
    

class MascotaPerdidaForm(forms.ModelForm):

    mascota = forms.ModelChoiceField(queryset=Mascota.objects.none())
    foto = forms.ImageField(validators=[validate_image], required=False) 
    fecha = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))
    
    class Meta: 
        model = MascotasPerdidas
        fields = ("contacto", "ultimo_lugar", "rasgos_particulares","descripcion", "fecha", "nombre", "raza")

    def __init__(self, usuario, *args, **kwargs):
        super(MascotaPerdidaForm, self).__init__(*args, **kwargs)
        self.fields['contacto'].required = True
        self.fields['ultimo_lugar'].required = True
        self.fields['rasgos_particulares'].required = True
        self.fields['descripcion'].required = True
        self.fields['fecha'].required = True
        self.fields['nombre'].required = True
        self.fields['raza'].required = True
        self.fields['mascota'].queryset = Mascota.objects.filter(dueno_id = usuario)
        
class MascotaNoRegistradaPerdidaForm(forms.ModelForm):

    foto = forms.ImageField(validators=[validate_image], required=False) 
    fecha = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))
    
    class Meta: 
        model = MascotasPerdidas
        fields = ("contacto", "ultimo_lugar", "rasgos_particulares","descripcion", "fecha", "nombre", "raza")

        

