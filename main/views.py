from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Mascota, Cliente, Mascota_Adopcion
from .form import UsuarioForm, MascotaAdopcionForm

from django.contrib.auth.mixins import LoginRequiredMixin




# Create your views here.

#Responde esto cuando quiere ver el:

# iniciar Sesion
def inisio_Sesion(request):
    return render(request,"inisio_Sesion.html")

# Menu principal
def main(request):
    """ Hay tres tipos de usuarios visitor , vet y client"""
    user = "visitor"
    context = {'user_type':user}
    return render(request, "index.html" , context)

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
    context = {'form':form, 'titulo': "Registro de Usuario"}

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
    
#SECCION DE LISTAS
from django.views import generic

#LoginRequiredMixin, 

#login_url = '/accounts/login/'
#redirect_field_name = 'redirect_to'
class AdopcionListView(generic.ListView):
    
    model = Mascota_Adopcion # Modelo al que le va a consultar los datos

    context_object_name = 'lista_mascotas_adopcion'   # your own name for the list as a template variable
    queryset = Mascota_Adopcion.objects.all() #Metodo que devuelve las mascotas, se puede poner un filter
    template_name = 'adopcion/lista_mascotas_adopcion.html'  # Specify your own template name/location

class MascotaListView(LoginRequiredMixin, generic.ListView):
    model = Mascota # Modelo al que le va a consultar los datos

    context_object_name = 'lista_mascotas'   # your own name for the list as a template variable
    queryset = Mascota.objects.all() #Metodo que devuelve las mascotas del usuario 1 solamente
    template_name = 'mis_mascotas/lista_mascotas.html'  # Specify your own template name/location
    paginate_by = 5

    def get_queryset(self):
        #return Mascota.objects.filter(dueno__correo=self.request.user).order_by('nombre')
        return Mascota.objects.filter(dueno__datos__nombre=self.request.user)

#SECCION DE LISTAS DE DETALLES

class AdopcionDetailView(generic.DetailView):
    model = Mascota_Adopcion
    template_name = 'adopcion/detalle_mascota.html'  # Specify your own template name/location

    def adopcion_detail_view(request,pk):
        try:
            mascota_adopcion_id=Mascota_Adopcion.objects.get(pk=pk)
        except Mascota_Adopcion.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/templates/adopcion/detalle_mascota.html',
            context={'mascota':mascota_adopcion_id}
        )
    
class MascotaDetailView(generic.DetailView):
    model = Mascota
    template_name = 'mis_mascotas/detalle_mascota.html'  # Specify your own template name/location

    def mascota_detail_view(request,pk):
        try:
            mascota_id=Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/templates/mis_mascotas/detalle_mascota.html',
            context={'mascota':mascota_id}
        )
    
@login_required
def registrar_adopcion(request):
    form = MascotaAdopcionForm()
    if request.method == "POST":
        form = MascotaAdopcionForm(request.POST)
        if form.is_valid():

            mi_objeto = form.save(commit=False)
            #Por ahora se los asignos al usuario 1
            mi_objeto.dueno = Cliente.objects.filter(pk=1)[0] # asignar el valor adicional al campo correspondiente
            # guardar el objeto en la base de datos

            #AGREGAR A FORM LOS DATOS DEL USUARIO
            print(mi_objeto.save())
            #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
            #form.save()
        
        return render(request, "index.html")
        print("\nSe registro a:\n")
        print()
    context = {'form':form, 'titulo': "Registro de Adopcion"}

    return render(request, "registro.html", context)

