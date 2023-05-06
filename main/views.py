from typing import Any
from django.views import generic
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Mascota, Cliente, Mascota_Adopcion, Turno
from .form import UsuarioForm, MascotaAdopcionForm, MascotaForm, TurnoForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST



from django.shortcuts import redirect
#from .form import RegistroForm
from .models import Persona

#Responde esto cuando quiere ver el:

# iniciar Sesion
def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        nombre_usuario = request.POST['nombre_usuario']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        contraseña_confir = request.POST['contraseña_confir']
        dni = request.POST['dni']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']

        if contraseña==contraseña_confir:
            if User.objects.filter(username=correo).exists():
                messages.info(request, 'El usuario ya existe, prueba otro')
                return redirect(registro)
            elif User.objects.filter(email=correo).exists():
                messages.info(request, 'Este correo ya esta registrado')
                return redirect(registro)
            else:
                user = User.objects.create_user(username=correo, password=contraseña, 
                                        email=correo, first_name=nombre, last_name=apellido)
                user.save()
                persona = Persona.objects.create(nombre = nombre,
                                                      apellido = apellido,
                                                      dni = dni,
                                                      direccion = direccion,
                                                      correo = correo,
                                                      telefono= telefono)
                cliente =Cliente.objects.create(usuario = user,
                                                datos = persona)
                
                return redirect('main')


        else:
            messages.info(request, 'Las contraseñas no son las mismas')
            return redirect(registro)
            

    else:
        return render(request, 'registro/registro.html')
    

def inicio_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']

        user = auth.authenticate(username=nombre_usuario, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Contraseña invalida o usuario incorrecto')
            return redirect('inicio de sesion')




    else:
        return render(request, 'registro/login.html')


def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario.
            return redirect('main')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contrasenia.html', {'form': form})

def cerrar_sesion(request):
    auth.logout(request)
    return redirect('main')

#Mi perfil
def perfil(request):

    cliente = Cliente.objects.filter(usuario__email=request.user.email)
    return (request, "perfil.html", {'cliente': cliente})

# Menu principal
def main(request):
    """ Hay tres tipos de usuarios visitor , vet y client"""
    user = "visitor"
    context = {'user_type':user}
    return render(request, "index.html" , context)

#Informacion sobre la veterinaria
def about(request):
    return render(request, "about.html")
"""
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

""" 


def registro1(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            print("se guardo")
            return render(request, 'index.html')
        else:
            print("NO se guardo")
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


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

    def get_queryset(self):
        #return Mascota.objects.filter(dueno__correo=self.request.user).order_by('nombre')
        return Mascota.objects.filter(dueno__usuario__email=self.request.user.email)
    queryset = get_queryset
    template_name = 'mis_mascotas/lista_mascotas.html'  # Specify your own template name/location
    paginate_by = 5
    
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()
    return redirect('Ver mis Mascotas')    

class MisAdopcionesListView(generic.ListView):
    
    model = Mascota_Adopcion # Modelo al que le va a consultar los datos

    context_object_name = 'mi_lista_mascotas_adopcion'   # your own name for the list as a template variable

    #Metodo que devuelve las mascotas
    def get_queryset(self):
        #return Mascota.objects.filter(dueno__correo=self.request.user).order_by('nombre')
        return Mascota_Adopcion.objects.filter(dueno__usuario__email=self.request.user.email)
    queryset = get_queryset

    template_name = 'mis_adopciones/lista_mis_adopciones.html'  # Specify your own template name/location

def marcar_adopcion(request, pk):
    perro = get_object_or_404(Mascota_Adopcion, pk=pk)
    perro.estado = 'a'
    perro.save()
    return redirect('ver mis adopciones')

class TurnosListView(generic.ListView):

    # Modelo al que le va a consultar los datos
    model = Turno 

    #Tu propio nombre para el template
    context_object_name = 'lista_de_turnos_pendientes'   

    #Metodo que devuelve los turnos sin confirmar
    def get_queryset(self):
        return Turno.objects.all()
    
    queryset = get_queryset

    #Especifica el lugar del template
    template_name = 'turnos/lista_de_turnos_pendientes.html' 




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
    
class TurnoDetailView(generic.DetailView):
    model = Turno
    template_name = 'turnos/detalle.html'  # Specify your own template name/location

    def turno_detail_view(request,pk):
        try:
            turno_id=Turno.objects.get(pk=pk)
        except Turno.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/templates/turnos/detalle.html',
            context={'mascota':turno_id}
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

@login_required
def registrar_mascota(request):
    form = MascotaForm()
    if request.method == "POST":
        form = MascotaForm(request.POST)
        if form.is_valid():

            mascota = form.save(commit=False)

            #Aca obtengo el dueño al que pertenece el usuarioi
            mascota.dueno = Cliente.objects.filter(datos__correo=request.user.email)[0] # asignar el valor adicional al campo correspondiente

            # guardar el objeto en la base de datos

            #AGREGAR A FORM LOS DATOS DEL USUARIO
            mascota.save()
            print("\nSe registro la mascota")
            #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
        
        return redirect("main")
        
    context = {'form':form, 'titulo': "Registro de Mascota"}

    return render(request, "registro.html", context)

@login_required
def solicitar_turno(request):
    form = TurnoForm()
    if request.method == "POST":
        form = TurnoForm(request.POST)
        if form.is_valid():

            turno = form.save(commit=False)

            #Aca obtengo el dueño al que pertenece el usuario
            turno.cliente = Cliente.objects.filter(usuario__email=request.user.email)[0] # asignar el valor adicional al campo correspondiente
            
            turno.asistio = False
           
            turno.aceptado = False
            # guardar el objeto en la base de datos

            #AGREGAR A FORM LOS DATOS DEL USUARIO
            turno.save()
            print("\nSe registro el turno")
            #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
        
            return redirect("main")
        else:
            print("\nNo se registro el turno")
            messages.info(request, 'Algo salio mal')
            return redirect('solicitar turno')
        
    context = {'form':form, 'titulo': "Solicitud de Turno"}

    return render(request, "registro.html", context)

