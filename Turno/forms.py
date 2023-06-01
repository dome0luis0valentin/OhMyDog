from django import forms

from .models import Veterinarias_de_turno

class VeterinariasForm(forms.ModelForm):  
    class Meta: 
        model = Veterinarias_de_turno 
        fields = ['arch']  
