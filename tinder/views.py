from django.shortcuts import get_object_or_404, render, redirect
from .forms import UsuarioTinderForm
from main.models import Cliente, Mascota
from .models import UsuarioTinder
from .validaciones import validar_existencia, validar_foto
from .funciones import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Mensaje import MENSAJE_DE_CONCIENCIA


@login_required
def enviar_solicitud(request, pk, mascota, hembra):
    perro_tinder = UsuarioTinder.objects.get(pk=pk)
    dueno_perro_tinder = perro_tinder.contacto
    enviar_notificación(dueno_perro_tinder, perro_tinder.mascota.nombre)
    return redirect("mostrar_coincidencias",mascota, hembra)

@login_required
def mostrar_coincidencias(request, mascota, hembra):
    coincidencias = obtener_coincidencias(mascota, hembra)

    return render(request, 'mostrar_coincidencias.html', {'coincidencias': coincidencias, 'mascota':mascota, 'hembra': hembra})

# Create your views here.
@login_required
def registrar(request):
    email =  request.user.email
    usuario = Cliente.objects.get(usuario__email = email)

    messages.info(request, MENSAJE_DE_CONCIENCIA)
    if request.method == "POST":
        # Valido los datos
        form = UsuarioTinderForm(usuario, email, request.POST, request.FILES)
        form.is_valid() 
        
        foto = request.FILES["foto"]
        foto_valida = validar_foto(foto)
        mascota = request.POST["mascota"]
        existe_mascota = validar_existencia(mascota)
        if "hembra" in request.POST:
            hembra = request.POST["hembra"] == "on"
        else:
            hembra= False
        fecha_celo_faltante = hembra and request.POST["fecha_de_celo"] == ""

        #Son correctos
        if form.is_valid() and not(existe_mascota) and not(fecha_celo_faltante) and foto_valida:
            mascota_tinder = registrar_mascota_tinder(form, mascota, hembra , usuario, foto)
            messages.success(request, "Se publico la mascota")


             # Genera la URL de destino con los parámetros
            url_destino = reverse('mostrar_coincidencias', args=[mascota, hembra])
            return redirect(url_destino)

        
   
        else: 
            agregar_errores(form, fecha_celo_faltante, existe_mascota, foto_valida)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:
       
        form = UsuarioTinderForm(usuario=usuario,email= email)
        context = {'form': form, 'titulo':"Registro de Mascota a Tinder de Perros"}
        return render(request, 'registrar_a_tinder.html', context)

@login_required
def ver_mis_mascotas(request):
    mascotas = UsuarioTinder.objects.filter(dueno__usuario__email = request.user.email, activa = True)
    return render(request, "lista_mascotas_tinder.html", {'mascotas':mascotas})

def dar_de_baja(request, pk):
    borrar_mascota_tinder(pk)
    messages.success(request, "Baja exitosa")
    return redirect('ver mis mascotas tinder')

def ver_mascotas(request):
    pass
