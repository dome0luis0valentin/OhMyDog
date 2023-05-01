from django.shortcuts import render

from .models import Mascota, Usuario
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
    

