from django import forms
from .models import UsuarioTinder
from main.models import Mascota


#En su inicialización se necesita una instancia de cliente y un email
class UsuarioTinderForm(forms.Form):
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.none())
    contacto = forms.CharField(max_length = 100)
    hembra = forms.BooleanField(required=False, label = "Es hembra: ")
    fecha_de_celo = forms.CharField(required=False, max_length = 200, label ="Fecha de celo")

    def __init__(self, usuario, email, *args, **kwargs):
        super(UsuarioTinderForm, self).__init__(*args, **kwargs)
        self.fields['contacto'].initial = email
        self.fields['mascota'].queryset = Mascota.objects.filter(dueno_id = usuario)