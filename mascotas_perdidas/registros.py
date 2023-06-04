from main.models import Cliente

def registrar_mascota_perdida(datos, email, foto):
    mascota=datos.save(commit=False)
    mascota.foto = foto
    cliente = Cliente.objects.get(usuario__email=email)
    mascota.cliente = cliente
    mascota.save()