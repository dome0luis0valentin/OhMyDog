from django import forms

class CampanaForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    motivo = forms.CharField(max_length=100)
    fecha_fin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'datepicker'}))
