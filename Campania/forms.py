from django import forms

class CampanaForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    motivo = forms.CharField(max_length=100)
    fecha_fin = forms.DateField()
