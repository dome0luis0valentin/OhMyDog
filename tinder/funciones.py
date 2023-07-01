from Mensaje import *
from .models import UsuarioTinder
from main.models import Mascota
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def agregar_errores(form, fecha, registrada):
    if fecha:
        form.errors['fecha_de_celo'] = [MENSAJE_FECHA_FALTANTE]

    if registrada:
        form.errors['mascota'] = [MENSAJE_MASCOTA_REGISTRADA]

def registrar_mascota_tinder(form, mascota, hembra , dueno_p):

    if UsuarioTinder.objects.filter(mascota__id = mascota).exists():
        mascota = UsuarioTinder.objects.get(mascota__id = mascota)
        mascota.activa = True

    else:
        mascota = Mascota.objects.get(id= mascota)
        mascota = UsuarioTinder.objects.create(mascota = mascota,
                                                hembra = hembra,
                                                fecha_de_celo = form.cleaned_data['fecha_de_celo'],
                                                contacto = form.cleaned_data['contacto'],
                                                dueno = dueno_p)
    mascota.save()
    return mascota

def obtener_coincidencias(mascota, hembra):
    raza = Mascota.objects.get(id = mascota).raza
    return UsuarioTinder.objects.filter(mascota__raza=raza, hembra = not(hembra)).exclude(mascota__id=mascota)

def enviar_notificación(user, datos):
    remitente = 'grupo21ing2@gmail.com'  # Dirección de correo electrónico del remitente
    asunto = "Tinder de Mascotas"
    mensaje = "Se ha registrado una potencial pareja para su mascota: "+datos # Contenido del mensaje

    email = EmailMessage(asunto, mensaje, to=[user])
    email.send()

def enviar_notificaciones(coincidencias, datos_mascota):
    datos_hembra = ""
    if datos_mascota.hembra == True:
        datos_hembra = f'Fecha de celo: {datos_mascota.fecha_de_celo}'
        
    datos = f'\n Nombre: {datos_mascota.mascota.nombre}\n Contacto:{datos_mascota.contacto}\n Fecha de Nacimiento: {datos_mascota.mascota.fecha_nac}\n'+datos_hembra
    for perro in coincidencias:
        usuario = perro.mascota.dueno.usuario.email
        enviar_notificación(usuario, datos)
 
def cargar_datos_mascota(mascotas_tinder):
    mascotas_datos = []
    for mascota_tinder in mascotas_tinder:
        mascota= Mascota.objects.get( id = mascota_tinder.mascota_id ) 
        mascotas_datos.append((mascota.nombre,mascota.color,mascota.fecha_nac,mascota.foto,mascota.id, mascota_tinder.pk))
    return mascotas_datos    

def borrar_mascota_tinder(pk):
    if (UsuarioTinder.objects.filter(pk=pk).exists()):
        mascota= UsuarioTinder.objects.get(pk=pk)
        mascota.activa = False
        mascota.save()