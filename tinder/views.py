from django.shortcuts import render, redirect
from .forms import UsuarioTinderForm
from main.models import Cliente, Mascota
from .models import UsuarioTinder
from .validaciones import validar_existencia
from .funciones import agregar_errores, registrar_mascota_tinder, obtener_coincidencias, enviar_notificaciones
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def registrar(request):
    email =  request.user.email
    usuario = Cliente.objects.get(usuario__email = email)
    if request.method == "POST":
        # Valido los datos
        form = UsuarioTinderForm(usuario, email, request.POST)
        form.is_valid()  
       
        
        mascota = request.POST["mascota"]
        existe_mascota = validar_existencia(mascota)
        if "hembra" in request.POST:
            hembra = request.POST["hembra"] == "on"
        else:
            hembra= False
        fecha_celo_faltante = hembra and request.POST["fecha_de_celo"] == ""

        #Son correctos
        if form.is_valid() and not(existe_mascota) and not(fecha_celo_faltante):
            mascota_tinder = registrar_mascota_tinder(form, mascota, hembra)
            messages.success(request, "Se publico la mascota")

            coincidencias = obtener_coincidencias(mascota, hembra)      
            enviar_notificaciones(coincidencias, mascota_tinder)

            return render(request, 'mostrar_coincidencias.html', {'coincidencias': coincidencias})
        
        #Datos erroneos
        else: 
            agregar_errores(form, fecha_celo_faltante, existe_mascota)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:
       
        form = UsuarioTinderForm(usuario=usuario,email= email)
        context = {'form': form, 'titulo':"Registro de Mascota a Tinder de Perros"}
        return render(request, 'registro.html', context)

def ver_mis_mascotas(request):
    pass

def dar_de_baja(request, id_mascota):
    pass

def ver_mascotas(request):
    pass
