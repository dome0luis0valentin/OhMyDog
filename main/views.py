from django.shortcuts import render

from .models import Mascota, Usuario, Mascota_Adopcion
from .form import UsuarioForm



# Create your views here.

#Responde esto cuando quiere ver el:

# Menu principal
def main(request):
    return render(request, "index.html")

#Informacion sobre la veterinaria
def about(request):
    return render(request, "about.html")
   
#Registrarse
def registro(request):

    form = UsuarioForm()
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
        print("\nSe registro a:\n")
        print(form.data["correo"])
    context = {'form':form}

    return render(request, "registro.html", context)

    

    #return render(request, "prueba_registro.html")

#Lista de Mascotas
def lista_mascota(request):
    #Forma basica:
    #return render(request, "prueba_lista_mascotas.html")

    #Esta seccion es compleja, lo que hace es mostrarte para cada usuario especifico sus 
    #mascotas
    #Aca tendría que filtrar todas las mascotas en adopcion
    lista = Mascota.objects.all()
    num_mascotas = Mascota.objects.all().count()
    main_data = {"lista": lista}
    return render(request, "lista_mascota.html", {"cantidad": num_mascotas, "lista":lista})
   
    


#Mostar detalle de mascota
def detalle_mascota(request, pk=None):

    return render(request, "prueba_detalle_mascota.html")

    #Forma compleja --> Hacer mas adelante
    """
    if pk:
        menu_item = Item.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, "menu_item.html", {"menu_item": menu_item})
    """
    

from django.views import generic

class AdopcionListView(generic.ListView):
    model = Mascota_Adopcion # Modelo al que le va a consultar los datos

    context_object_name = 'lista_mascotas_adopcion'   # your own name for the list as a template variable
    queryset = Mascota_Adopcion.objects.all() #Metodo que devuelve las mascotas, se puede poner un filter
    template_name = 'lista_mascotas_adopcion.html'  # Specify your own template name/location

class AdopcionDetailView(generic.DetailView):
    model = Mascota_Adopcion
    template_name = 'detalle_mascota.html'  # Specify your own template name/location

    def adopcion_detail_view(request,pk):
        try:
            mascota_adopcion_id=Mascota_Adopcion.objects.get(pk=pk)
        except Mascota_Adopcion.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/detalle_mascota.html',
            context={'mascota':mascota_adopcion_id,}
        )