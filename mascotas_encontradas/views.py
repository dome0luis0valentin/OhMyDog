from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import Cliente
from Funciones import fecha_anterior_is_valid
from .registros import registrar_mascota_encontrada
from Mensaje import *
from .funciones import agregar_errores
from .models import MascotasEncontradas
from django.views import generic
from .forms import MascotaEncontradaForm
# Create your views here.
 
@login_required
def publicar(request):
    form = MascotaEncontradaForm()
    
    if request.method == "POST":
        # Valido los datos  
        form = MascotaEncontradaForm(request.POST, request.FILES)
        
        #Son correctos
        if form.is_valid():
            registrar_mascota_encontrada(form,request.FILES["foto"], request.user.email)
            messages.success(request, "Se publico la mascota")
            return redirect('menu')
        
        #Datos erroneos
        else: 
            agregar_errores(form)

            context = {'form': form, 'titulo': "Publicar Mascota Encontrada"}
            return render(request, 'registro.html', context)
    else:
        
        # Solicito los datos
        context = {'form': form, 'titulo': "Publicar Mascota Encontrada"}
        return render(request, 'registro.html', context)


def ver_encontrados(request):
    lista = MascotasEncontradas.objects.all()
    return render(request, "encontrados.html", {"lista":lista})
   

class EncontradosDetailView(generic.DetailView):
    model = MascotasEncontradas
    template_name = 'detalle_encontrados.html' 

    def encontrados_detail_view(request,pk):
        try:
            mascota=MascotasEncontradas.objects.get(pk=pk)
        except MascotasEncontradas.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")
        
        print(mascota)
        return render(
            request,
            'detalle_encontrados.html',
            context={'mascota':mascota}
        )

@login_required
def marcar_devuelto(request, pk): 
    perro = MascotasEncontradas.objects.get(pk=pk)
    perro.devuelto = True
    perro.save()
    return redirect('ver mis encontrados')

@login_required
def ver_mis_encontrados(request):
    lista = MascotasEncontradas.objects.filter(cliente__usuario__email=request.user.email)
    return render(request, "mis_encontrados.html", {"lista":lista})
   


    