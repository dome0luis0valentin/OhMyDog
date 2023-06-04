from django.shortcuts import render, redirect
from .forms import MascotaPerdidaForm, MascotaNoRegistradaPerdidaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import Cliente
from Funciones import fecha_anterior_is_valid
from .registros import registrar_mascota_perdida
from Mensaje import *
from .funciones import agregar_errores
from .models import MascotasPerdidas
from django.views import generic
# Create your views here.
 
def menu(request):
    user = "visitor"
    context = {'user_type':user}
    return render(request, "menu.html" , context)

@login_required
def publicar(request):

    cliente= Cliente.objects.get(usuario=request.user)
    usuario = cliente.id 
    form = MascotaPerdidaForm(usuario)
    
    if request.method == "POST":
        # Valido los datos  
        form = MascotaPerdidaForm(usuario, request.POST, request.FILES)
        fecha_valida = fecha_anterior_is_valid(request.POST["fecha"])
       
        #Son correctos
        if form.is_valid() and fecha_valida:
            
            registrar_mascota_perdida(form, request.user.email, request.FILES["foto"])
            messages.success(request, "Se publico la mascota")
            return redirect('menu')
        
        #Datos erroneos
        else: 
            agregar_errores(form, fecha_valida)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:
        
        # Solicito los datos
        context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
        return render(request, 'registro.html', context)


@login_required
def publicar_no_registrada(request):

     
    form = MascotaNoRegistradaPerdidaForm()
    
    if request.method == "POST":
        # Valido los datos
       
        form = MascotaNoRegistradaPerdidaForm(request.POST, request.FILES)
        fecha_valida = fecha_anterior_is_valid(request.POST["fecha"])
       
        
        #Son correctos
        if form.is_valid() and fecha_valida:
            registrar_mascota_perdida(form, request.user.email, request.FILES["foto"])

            messages.success(request, "Se publico la mascota")
            return redirect('menu')
        
        #Datos erroneos
        else: 
            agregar_errores(form, fecha_valida)

            context = {'form': form, 'titulo': "Publicar Mascota Perdida"}
            return render(request, 'registro.html', context)
    else:
        
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
    perro = MascotasPerdidas.objects.get(pk=pk)
    perro.encontrado = True
    perro.save()
    return redirect('ver mis perididos')

@login_required
def ver_mis_perdidos(request):
    lista = MascotasPerdidas.objects.filter(cliente__usuario__email=request.user.email)
    return render(request, "mis_perdidos.html", {"lista":lista})
   


    