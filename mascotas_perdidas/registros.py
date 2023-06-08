from main.models import Cliente, Mascota


def registrar_mascota_perdida(datos, email, foto):
    mascota=datos.save(commit=False)
    mascota.foto = foto
    cliente = Cliente.objects.get(usuario__email=email)
    mascota.cliente = cliente
    mascota.save()

def registrar_mascota_registrada_perdida(form, datos, foto):
    mascota_per=form.save(commit=False)
    mascota_per.foto = foto
    id_mascota = datos.POST["mascota"]
    mascota = Mascota.objects.get(id=id_mascota)
    mascota.perdida = True
    mascota_per.nombre = mascota.nombre
    mascota_per.raza = mascota.raza
    cliente = Cliente.objects.get(usuario__email=datos.user.email)
    mascota_per.cliente = cliente
    mascota_per.save()