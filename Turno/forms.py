from django import forms

from .models import Veterinarias_de_turno

class VeterinariasForm(forms.ModelForm):  
    class Meta: 
        model = Veterinarias_de_turno 
        fields = ['arch']  


class FormularioSimple(forms.Form):
    descripcion = forms.CharField(label='Descripcion', max_length=100)
    monto = forms.DecimalField(label="Monto a cobrar", max_digits=6, decimal_places=3)
    
    


class DesparasitanteForm(forms.Form):
    peso = forms.DecimalField(label="Peso en Kg", max_digits=6, decimal_places=3)
    codigo = forms.CharField(label="Código del desparasitante")
    cantidad = forms.IntegerField(label="Cantidad")
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea)
    monto = forms.DecimalField(label="Monto a cobrar", max_digits=6, decimal_places=3)
    
class VacunacionForm(forms.Form):
    peso = forms.DecimalField(label="Peso en Kg", max_digits=6, decimal_places=3)
    codigo = forms.CharField(label="Código del la vacuna")
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea)
    monto = forms.DecimalField(label="Monto a cobrar", max_digits=6, decimal_places=3)    