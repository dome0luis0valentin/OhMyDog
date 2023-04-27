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
        print("\n-------Datos-------\n")
        print(form.data["correo"])
    context = {'form':form}

    return render(request, "registro.html", context)

    

    #return render(request, "prueba_registro.html")

#Lista de Mascotas
def lista_mascotas(request):
    #Forma basica:
    return render(request, "prueba_lista_mascotas.html")

    #Esta seccion es compleja, lo que hace es mostrarte para cada usuario especifico sus 
    #mascotas
    """
    lista = Mascota.objects.all()
    main_data = {"lista": lista}
    return render(request, "lista_mascotas.html", {"lista": main_data})
    
    """
    


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
    