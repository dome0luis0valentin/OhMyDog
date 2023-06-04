from main.models import Cliente

def registrar_mascota_encontrada(datos, foto, email):
    mascota=datos.save(commit=False)
    cliente = Cliente.objects.get(usuario__email=email)
    mascota.cliente = cliente
    mascota.foto = foto
    mascota.save()