from main.models import Cliente
from tinder.models import UsuarioTinder
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_existencia(id_mascota):
    if UsuarioTinder.objects.filter(mascota__id = id_mascota).exists():
        mascota = UsuarioTinder.objects.get(mascota__id = id_mascota)
        return mascota.activa
    return False

def validar_foto(foto):
    extension = foto.name.split('.')[-1].lower()
    allowed_extensions = ['png', 'jpeg', 'jpg']

    if extension not in allowed_extensions:
        return False
        raise ValidationError(_('El archivo debe ser de tipo PNG, JPEG o JPG.'))
    else:
        return True
