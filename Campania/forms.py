from django import forms
from django.core.exceptions import ValidationError

class CampanaForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    motivo = forms.CharField(max_length=100)
    fecha_fin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))
    nombre = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Nombre'}))
    motivo = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Motivo'}))

from django.core.exceptions import ValidationError

class TarjetaCreditoField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if not value.isdigit():
            raise ValidationError('El número de tarjeta debe contener solo dígitos.')
        return value

class PagoForm(forms.Form):
    numero_de_tarjeta = TarjetaCreditoField()
    cantidad = forms.DecimalField(max_digits=6, decimal_places=2)
    numero_de_tarjeta = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Numnero de tarjeta'}))
    cantidad = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Cantidad a donar'}))



'''
class PagoForm(forms.Form):
    numero_de_tarjeta = forms.IntegerField(
        widget=forms.TextInput(attrs={'maxlength': '16'}),
        min_value=0,
        max_value=9999999999999999
    )
    cantidad = forms.DecimalField(max_digits=6, decimal_places=2)
'''