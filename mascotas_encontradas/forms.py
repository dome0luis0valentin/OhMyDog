from django import forms

from .models import MascotasEncontradas
from main.models import Mascota

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image(file):
    if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
        raise ValidationError(
            _('El archivo subido no es una imagen válida.')
        )
    

class MascotaEncontradaForm(forms.ModelForm):
    class Meta: 
        model = MascotasEncontradas
        fields = ("descripcion","foto","contacto", "direccion")
        labels = {
            'cliente': 'Ingrese el nombre del cliente',
            'descripcion': 'Ingrese la descripción de la mascota',
            'foto': 'Seleccione una foto',
            'contacto': 'Ingrese la información de contacto',
            'direccion': 'Ingrese la dirección',
        }  

        

