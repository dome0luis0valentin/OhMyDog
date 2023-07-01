from main.models import Cliente
from tinder.models import UsuarioTinder

def validar_existencia(id_mascota):
    if UsuarioTinder.objects.filter(mascota__id = id_mascota).exists():
        mascota = UsuarioTinder.objects.get(mascota__id = id_mascota)
        return mascota.activa
    return False