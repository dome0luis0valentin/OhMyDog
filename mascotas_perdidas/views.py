from django.shortcuts import render, redirect
from .forms import MascotaPerdidaForm, MascotaNoRegistradaPerdidaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import Cliente, Mascota
from Funciones import fecha_anterior_is_valid
from .registros import registrar_mascota_perdida,registrar_mascota_registrada_perdida
from Mensaje import *
from .funciones import agregar_errores
from .models import MascotasPerdidas
from django.views import generic
from .validaciones import mascota_perdida, validar_existencia
# Create your views here.
 
def menu(request):
    user = "visitor"
    context = {'user_type':user}
    return render(request, "menu.html" , context)

@login_required
def publicar(request):  
    if request.method == "POST":
        cliente= Cliente.objects.get(usuario=request.user)
        usuario = cliente.id
        email = cliente.usuario.email

        # Valido los datos  
        form = MascotaPerdidaForm(usuario, email, request.POST, request.FILES)
        fecha_valida = fecha_anterior_is_valid(request.POST["fecha"])
        mascota = Mascota.objects.get(id=request.POST["mascota"])

        nombre_mascota = Mascota.objects.get(id=request.POST["mascota"])
        existe_mascota = validar_existencia(email, nombre_mascota)

        
        #Son correctos
        if form.is_valid() and fecha_valida and not(existe_mascota):
            
            registrar_mascota_registrada_perdida(form, request, request.FILES["foto"])
            messages.success(request, "Se publico la mascota")
            return redirect('menu')
        
        #Datos erroneos
        else: 
            agregar_errores(form, fecha_valida, existe_mascota)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:   
        cliente= Cliente.objects.get(usuario=request.user)
        usuario = cliente.id 
        email = cliente.usuario.email
        
        form = MascotaPerdidaForm(usuario, email) 
        # Solicito los datos
        context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
        return render(request, 'registro.html', context)


@login_required
def publicar_no_registrada(request):
    if request.method == "POST":
        # Valido los datos
       
        form = MascotaNoRegistradaPerdidaForm(request.user.email, request.POST, request.FILES)
        fecha_valida = fecha_anterior_is_valid(request.POST["fecha"])

        existe_mascota = validar_existencia(request.user.email, nombre=request.POST["nombre"])
       
        
        #Son correctos
        if form.is_valid() and fecha_valida and not(existe_mascota):
            registrar_mascota_perdida(form, request.user.email, request.FILES["foto"])

            messages.success(request, "Se publico la mascota")
            return redirect('menu')
        
        #Datos erroneos
        else: 
            agregar_errores(form, fecha_valida, existe_mascota)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:
        form = MascotaNoRegistradaPerdidaForm(request.user.email)
        # Solicito los datos
        context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
        return render(request, 'registro.html', context)

@login_required
def ver_perdidos(request):
    lista = MascotasPerdidas.objects.all()
    return render(request, "perdidos.html", {"lista":lista})
   

class PerdidosDetailView(generic.DetailView):
    model = MascotasPerdidas
    template_name = 'detalle_perdidas.html' 

    def perdidos_detail_view(request,pk):
        try:
            mascota=MascotasPerdidas.objects.get(pk=pk)
        except MascotasPerdidas.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")
        
        print(mascota)
        return render(
            request,
            'detalle_perdidas.html',
            context={'mascota':mascota}
        )

@login_required
def marcar_encontrado(request, pk): 
    print("Clave a borrar", pk)
    perro = MascotasPerdidas.objects.get(pk=pk)
    perro.encontrado = True
    perro.save()
    print("estado: ")
    print(perro.encontrado)
    return redirect('ver mis perididos')

@login_required
def ver_mis_perdidos(request):
    lista = MascotasPerdidas.objects.filter(cliente__usuario__email=request.user.email)
    return render(request, "mis_perdidos.html", {"lista":lista})
   


    