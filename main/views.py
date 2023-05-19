from typing import Any
from django.views import generic
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta

from django.core.paginator import Paginator

from datetime import datetime

from .models import Mascota,Intentos, Cliente, Mascota_Adopcion, Red_Social, Turno, Prestador_Servicios, Vacuna_tipoA , Vacuna_tipoB
from .form import UrgenciaForm,UsuarioForm, MascotaAdopcionForm,Red_SocialForm , MascotaForm, TurnoForm, ServicioForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import render, redirect

#Usuario viejo de Django
#from django.contrib.auth.models import User
from django.contrib.auth.models import auth
#Usuario nuevo personalizado
from main.models import User


from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import redirect
#from .form import RegistroForm
from .models import Persona

import re

from validate_email_address import validate_email

import random
import string

def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(10))
    return contrasena


def enviar_nueva_contraseña(user):
    remitente = 'grupo21ing2@gmail.com'  # Dirección de correo electrónico del remitente
    nueva_contraseña = generar_contrasena()
    mensaje = "Esta es tu nueva contraseña: "+nueva_contraseña  # Contenido del mensaje

    email = EmailMessage("Desbloquear usuario", mensaje, to=[user])
    email.send()

    return nueva_contraseña

def cadena_is_valid(cadena):
    if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$", cadena):
        return False
    return True

def numero_is_valid(numero):
    try:
        num = int(numero)
        return num>0
    except:
        return False

def todos_numeros(*cadenas):
    for cadena in cadenas:
        if not cadena.isdigit():
            return False
    return True

def todos_cadenas(*cadenas):
    for cadena in cadenas:
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$", cadena):
            return False
    return True

def dni_is_valid(dni):
    try:
        dni = int(dni)
        return True
    except:
        return False
    
def fecha_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada >= hoy
    except:
        # El usuario no existe en la base de datos
        return False
    
def fecha_anterior_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada <= hoy
    except:
        # El usuario no existe en la base de datos
        return False
    

def usuario_is_valid(username):
    try:
        user = User.objects.get(email=username)
        # El usuario existe en la base de datos
        return True
    except User.DoesNotExist:
        # El usuario no existe en la base de datos
        return False


MENSAJE_FECHA_INVALIDA = 'Verifique que la fecha tenga el formato AAAA-MM-DD y que sea un dia valido. Ejemplo: 2023-01-01'
MENSAJE_USUARIO_INVALIDO = 'Usuario incorrecto, revise que el email sea correcto y que el cliente este registrado'
MENSAJE_SOLO_LETRAS = 'Solo se permiten letras, no ingrese numeros, ni simbolos como #,$,/, etc.'
MENSAJE_SOLO_NUMEROS = "Solo se permiten números, no ingrese simbolos como .,-, /, etc."
# iniciar Sesion

def inicio_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']

        user = auth.authenticate(username=nombre_usuario, password=password)
        print(user)
        
        existe = Cliente.objects.filter(usuario__email=nombre_usuario).exists()

        if (existe):
            intentos=Intentos.objects.filter(usuario=nombre_usuario)

            #Inicializo los intento si el usuario es nuevo
            if(len(intentos) == 0):
                intento = Intentos.objects.create(usuario = nombre_usuario,
                                                  cantidad = 0,
                                                  estado = 'n')   
            else:
                intento = intentos[0]

        #Si la contraseña o usuario no son validos
        if user is  None:
            if not(existe):
                messages.info(request, 'Contraseña invalida o usuario incorrecto')
            else:
                #Si el usuario existe le incremento la cantidad de intentos fallidos.
                if (intento.cantidad < 3):
                    intento.cantidad = intento.cantidad +1
                    intento.save()
                    messages.info(request, 'Contraseña invalida o usuario incorrecto')
                    return redirect('inicio de sesion')
                #Si el usuario esta bloqueado
                else:
                    if (intento.estado == 'n'):
                        usuario = User.objects.get(username=nombre_usuario)
                        usuario.set_password(enviar_nueva_contraseña(nombre_usuario))
                        usuario.save()
                    intento.estado = 'b'
                    intento.save() 
                           
                    messages.info(request, 'Usuario bloqueado, revise su email para desbloquearlo')
                    
            return redirect('inicio de sesion')          
        #si todo esta bien
        else:
            auth.login(request, user)
            intento.cantidad=0
            intento.save()
            render(request, "index.html")
    else:            
        return render(request, 'registro/login.html')
    return redirect('inicio de sesion')

def usuario_bloqueado(request):
    return render(request, 'usuario_bloqueado.html')

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

def confirmar_cambiar_contraseña(request):
    return render(request, 'confirmar.html', {'accion': "cambiar contraseña", 'direccion': "cambiar_contraseña"})

def cerrar_sesion(request):   
    if request.method == 'POST' and request.POST.get('confirmar') == '1':
        auth.logout(request)
        return redirect('main')
    else:
        return redirect('main')

def confirmar_cerrar_sesion(request):
    return render(request, 'confirmar.html',{'accion': "cerrar secion", 'direccion': "cerrar_sesion"})

#Mi perfil
def perfil(request):
    cliente = Cliente.objects.filter(usuario__email=request.user.email)[0]
    mascotas = Mascota.objects.filter(dueno__usuario__email =request.user.email)
    return render(request, "perfil.html", {'cliente': cliente, 'mascotas': mascotas})

# Menu principal
def main(request):
    user = "visitor"
    context = {'user_type':user}
    return render(request, "index.html" , context)

#Informacion sobre la veterinaria
def about(request):
    return render(request, "about.html")

#Lista de Mascotas
def lista_mascota(request):
    #Forma basica:
    #return render(request, "prueba_lista_mascotas.html")

    #Esta seccion es compleja, lo que hace es mostrarte para cada usuario especifico sus 
    #mascotas
    #Aca tendría que filtrar todas las mascotas en adopcion
    lista = Mascota.objects.all()
    num_mascotas = Mascota.objects.filter(dueno__usuario__email = auth.user.email)
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

def confirmar_eliminar_mascota(request, mascota_id):
    return render(request,'mis_mascotas/confirmar_eliminar.html', {'id': mascota_id, 'accion': "eliminar mascota"})

def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    messages.success(request, f'Se ha dado de baja a : "{mascota.nombre}" ')
    mascota.delete()
    return redirect('Ver mis Mascotas')    

def marcar_adopcion(request, pk):
    perro = get_object_or_404(Mascota_Adopcion, pk=pk)
    perro.estado = 'a'
    perro.save()
    return redirect('ver mis adopciones')


def formulario_adopcion(request):
    return render(request,"formulario_adopcion.html")


def enviar_formulario_adopcion(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        motivo = request.POST.get('motivo')

        if (dni_is_valid(dni)):
            # Renderizar la plantilla de correo electrónico
            html_message = render_to_string('email_template.html', {'nombre': nombre, 'apellido': apellido, 'dni': dni, 'correo': correo, 'telefono': telefono, 'motivo': motivo})
            plain_message = strip_tags(html_message)

            # Enviar el correo electrónico
            send_mail(
                'Formulario de adopción',
                plain_message,
                'grupo21ing2@gmail.com',
                # tendriamos que agregar el gmail del usuario que publico la adopcion mejor dicho el dueño del perro
                ['josuecarrera788@gmail.com'],
                html_message=html_message,
            )

            # Redireccionar a una página de éxito
            return redirect('adopciones')
        else:
            messages.error(request,"DNI invalido, solo ingrese numeos, sin puntos ni espacios ")
            return redirect('adopciones')
    else:
        
        return render(request, 'formulario_adopcion.html') 
    
def rechazar_turno(request, turno_id):
    if request.method == 'POST':
        #rechazar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='A'
        turno.save()

        return redirect('confirmar turnos')
        

def aceptar_turno(request, turno_id):
    if request.method == 'POST':
        #aceptar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='R'
        turno.save()

        return redirect('confirmar turnos')



#-----------------------------SECCION DE LISTAS-------------------------------------


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
    paginate_by = 6
    

class MisAdopcionesListView(generic.ListView):
    
    model = Mascota_Adopcion # Modelo al que le va a consultar los datos

    context_object_name = 'mi_lista_mascotas_adopcion'   # your own name for the list as a template variable

    #Metodo que devuelve las mascotas
    def get_queryset(self):
        #return Mascota.objects.filter(dueno__correo=self.request.user).order_by('nombre')
        return Mascota_Adopcion.objects.filter(dueno__usuario__email=self.request.user.email)
    queryset = get_queryset

    template_name = 'mis_adopciones/lista_mis_adopciones.html'  # Specify your own template name/location


class TurnosListView(generic.ListView):

    # Modelo al que le va a consultar los datos
    model = Turno 

    #Tu propio nombre para el template
    context_object_name = 'lista_de_turnos_pendientes'   

    #Metodo que devuelve los turnos sin confirmar
    def get_queryset(self):
        return Turno.objects.filter(estado='E')
    
    queryset = get_queryset

    #Especifica el lugar del template
    template_name = 'turnos/lista_de_turnos_pendientes.html' 

class ServiciosListView(generic.ListView):
    # Modelo al que le va a consultar los datos
    model = Prestador_Servicios 

    #Tu propio nombre para el template
    context_object_name = 'lista_de_servicios'   

    #Metodo que devuelve los turnos sin confirmar
    def get_queryset(self):
        return Prestador_Servicios.objects.all()
    
    queryset = get_queryset

    #Especifica el lugar del template
    template_name = 'servicios/lista_de_servicios.html' 




#-----------------SECCION DE LISTAS DE DETALLES----------------------

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

    paginate_by = 3
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
    
class ServicioDetailView(generic.DetailView):
    model = Prestador_Servicios
    template_name = 'servicios/detalle.html'  # Specify your own template name/location

    def servicio_detail_view(request,pk):
        try:
            servicio_id=Prestador_Servicios.objects.get(pk=pk)
        except Prestador_Servicios.DoesNotExist:
            raise Http404("Esta mascota no esta registrada")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/templates/servicios/detalle.html',
            context={'servicio':servicio_id}
        )
    
@login_required
def registrar_adopcion(request):
    form = MascotaAdopcionForm()
    if request.method == "POST":
        form = MascotaAdopcionForm(request.POST)

        fecha = request.POST['fecha_nac']
        nombre = request.POST['nombre']
        color = request.POST['color']
        raza = request.POST['raza']
        ingreso_solo_letras = todos_cadenas(nombre, color, raza)
        fecha_es_anterior_a_hoy = fecha_anterior_is_valid(fecha)
        if form.is_valid() and fecha_es_anterior_a_hoy  and ingreso_solo_letras:

            mi_objeto = form.save(commit=False)
            
            mi_objeto.dueno = Cliente.objects.filter(usuario__email=request.user.email)[0]
            # guardar el objeto en la base de datos

            #AGREGAR A FORM LOS DATOS DEL USUARIO
            print(mi_objeto.save())
            #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
            #form.save()
            messages.info(request, "Mascota registrada")
            return render(request, "index.html")
        else:
            # Verificar errores y mostrar mensajes personalizados

            if not fecha_es_anterior_a_hoy:
                form.errors['fecha_nac'] = [MENSAJE_FECHA_INVALIDA]

            if not cadena_is_valid(nombre):
                form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]

            if not cadena_is_valid(raza):
                form.errors['raza'] = [MENSAJE_SOLO_LETRAS]
            
            if not cadena_is_valid(color):
                form.errors['color'] = [MENSAJE_SOLO_LETRAS]

    context = {'form':form, 'titulo': "Registro de Adopcion"}

    return render(request, "registro.html", context)

@login_required
def registrar_servicio(request):

    form = ServicioForm()
    red_form = Red_SocialForm()


    if request.method == "POST":
        form = ServicioForm(request.POST)
        red_form = Red_SocialForm(request.POST) 

        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        tipo = request.POST['tipo']
        correo = request.POST['correo']
        dni = request.POST['dni']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']

        son_todos_cadenas = todos_cadenas(nombre, apellido)
        son_todos_numeros = todos_numeros(telefono, dni)

        if form.is_valid() and red_form.is_valid() and son_todos_cadenas and son_todos_numeros:
        
            if not(Prestador_Servicios.objects.filter(datos__correo=correo).exists()):
                red = red_form.save(commit=False)

                persona = Persona.objects.create(nombre = nombre,
                                                apellido = apellido,
                                                dni = dni,
                                                direccion = direccion,
                                                correo = correo,
                                                telefono= telefono)
                persona.save()
                
                prestador_de_servicios = Prestador_Servicios.objects.create(datos = persona,
                                                    tipo = tipo)
                prestador_de_servicios.save()
                
                red.dueno = prestador_de_servicios
                messages.success(request,"Se registro el servicio")
                return redirect('main')

                print("\nSe registro un servicio")
            else:
                form.errors['correo'] = ["El usuario ya existe"]
        else:
             # Verificar errores y mostrar mensajes personalizados

            if not cadena_is_valid(nombre):
                form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]
            
            if not cadena_is_valid(apellido):
                form.errors['apellido'] = [MENSAJE_SOLO_LETRAS]

            if not numero_is_valid(dni):
                form.errors['dni'] = [MENSAJE_SOLO_NUMEROS]
            
            if not numero_is_valid(telefono):
                form.errors['telefono'] = [MENSAJE_SOLO_NUMEROS]

    context = {'form':form,'red_form': red_form, 'titulo': "Registro de Servicios de Terceros"}

    return render(request, "registro_servicio.html", context)


@login_required
def registrar_urgencia(request):
    form = UrgenciaForm()
   
    if request.method == "POST":
        form = UrgenciaForm(request.POST) 

        banda_horaria = request.POST['banda_horaria']
        fecha = request.POST['fecha']
        motivo = request.POST['motivo']
        correo_cliente = request.POST['cliente']

        if form.is_valid() and fecha_is_valid(fecha) and usuario_is_valid(correo_cliente):
            
            urgencia = form.save(commit=False)

            cliente= Cliente.objects.filter(usuario__email=correo_cliente)[0]

            urgencia = Turno.objects.create(cliente = cliente,
                                                fecha = fecha,
                                                banda_horaria = banda_horaria,
                                                motivo = motivo,
                                                asistio = True,
                                                estado = 'A')
            urgencia.save()

            print("\nSe registro la urgencia")
                #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
            
            return redirect("main")
        else:
            if 'fecha' in form.errors or not (fecha_is_valid(fecha)):
                messages.info(request, MENSAJE_FECHA_INVALIDA)
            if not (usuario_is_valid(correo_cliente)):
                messages.info(request, MENSAJE_USUARIO_INVALIDO)
            print("\n NO Se registro la urgencia")
            return redirect('registrar urgencia')

    context = {'form':form, 'titulo': "Registro de Servicios de Urgencias"}

    return render(request, "registro.html", context)


@login_required
def registrar_mascota(request):
    form = MascotaForm()
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)

        fecha = request.POST['fecha_nac']
        nombre = request.POST['nombre']
        color = request.POST['color']
        raza = request.POST['raza']

        ingreso_solo_letras = todos_cadenas(nombre, color, raza)
        fecha_es_anterior_a_hoy = fecha_anterior_is_valid(fecha)
        if form.is_valid() and fecha_es_anterior_a_hoy  and ingreso_solo_letras:
            
            mascota = form.save(commit=False)

            if 'foto' in request.FILES:
                mascota.foto = request.FILES['foto']
            mascota.fecha_nac =fecha
            #Aca obtengo el dueño al que pertenece el usuario
            mascota.dueno = Cliente.objects.filter(datos__correo=request.user.email)[0] # asignar el valor adicional al campo correspondiente

            mascota.save()
            #Si todo salio bien vuelve al menu principal
            return redirect("main")  

        # Verificar errores y mostrar mensajes personalizados

        if not fecha_es_anterior_a_hoy:
            form.errors['fecha_nac'] = [MENSAJE_FECHA_INVALIDA]

        if not cadena_is_valid(nombre):
            form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]

        if not cadena_is_valid(raza):
            form.errors['raza'] = [MENSAJE_SOLO_LETRAS]
        
        if not cadena_is_valid(color):
            form.errors['color'] = [MENSAJE_SOLO_LETRAS]

        if form.errors:
            for field_name, errors in form.errors.items():
                if (field_name == 'foto'):
                    form.errors['foto'] = ["Imagen invalida, verifique que el archivo sea de tipo .jpg, .png o jpeg"]
                    
    context = {'form':form, 'titulo': "Registro de Mascota"}
    return render(request, "registro.html", context)


def mascota_cumple(mascota ,fecha, tipo):
    if tipo == "A" :
        if Vacuna_tipoA.objects.filter(mascota_id = mascota.id).exists() :
            fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
            edad_meses = (fecha_ingresada.year - mascota.fecha_nac.year) * 12 + fecha_ingresada.month - mascota.fecha_nac.month
            vacuna = Vacuna_tipoA.objects.get(mascota_id = mascota.id)           
            if edad_meses > 2 and edad_meses < 4 :
                if fecha_ingresada > vacuna.fecha_aplicacion + timedelta(days=21) :
                    return True  
            elif edad_meses > 4 :
                if fecha_ingresada > vacuna.fecha_aplicacion + relativedelta(years=1) :
                    return True
            else :
                return False
        return True        
    elif tipo == "B":
        if Vacuna_tipoB.objects.filter(mascota_id = mascota.id).exists() :
            fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
            edad_meses = (fecha_ingresada.year - mascota.fecha_nac.year) * 12 + fecha_ingresada.month - mascota.fecha_nac.month
            vacuna = Vacuna_tipoB.objects.get(mascota_id = mascota.id)           
            if edad_meses > 4 :
                if fecha_ingresada > vacuna.fecha_aplicacion + relativedelta(years=1) :
                    return True
            else :
                return False
        return True
    return True        
        
@login_required
def solicitar_turno(request):
    
    cliente= Cliente.objects.get(usuario=request.user)
    cliente_dueño = cliente.id 
    
    form = TurnoForm(cliente_dueño)

    if request.method == "POST":
        
        form = TurnoForm(cliente_dueño,request.POST)

        fecha = request.POST["fecha"]
        
        mascota_id = request.POST["mascota"]
        
        mascota = get_object_or_404(Mascota, id=mascota_id)
        
        motivo = request.POST["motivo"]

        #Python no valida todo el condicional, si el form no es valido no valida la fecha
        if form.is_valid() and fecha_is_valid(fecha) and mascota_cumple(mascota,fecha,motivo):

            turno = form.save(commit=False)

            #Aca obtengo el dueño al que pertenece el usuario
            turno.cliente = Cliente.objects.filter(usuario__email=request.user.email)[0] # asignar el valor adicional al campo correspondiente
            
            turno.asistio = False
           
            turno.estado = 'E'
            # guardar el objeto en la base de datos

            #AGREGAR A FORM LOS DATOS DEL USUARIO
            turno.save()
            print("\nSe registro el turno")
            #ACA SE REGISTRA EN LA BASE DE DATOS PERO HAY QUE AGREGAR DATOS DE USUARIO
        
            return redirect("main")
        else:
            print("\nNo se registro el turno")
           
            messages.info(request, MENSAJE_FECHA_INVALIDA)
            return redirect('solicitar turno')
        
    context = {'form':form, 'titulo': "Solicitud de Turno"}

    return render(request, "registro.html", context)

@login_required
def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        contraseña_confir = request.POST['contraseña_confir']
        dni = request.POST['dni']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        is_veterinario = request.POST.get('is_veterinario')

        is_veterinario = (is_veterinario=='on')

        son_todos_letras = todos_cadenas(nombre, apellido)
        son_todos_numeros = todos_numeros(telefono, dni)

        
        correo_existe = (True == validate_email(correo, verify=True)) 

        if contraseña==contraseña_confir and son_todos_numeros and son_todos_letras and correo_existe:
            if User.objects.filter(username=correo).exists():
                messages.info(request, 'El usuario ya existe, prueba otro')
                return redirect(registro)
            elif User.objects.filter(email=correo).exists():
                messages.info(request, 'Este correo ya esta registrado')
                return redirect(registro)
            else:
                user = User.objects.create_user(username=correo,
                                                password=contraseña, 
                                                email=correo,
                                                first_name=nombre,
                                                last_name=apellido,
                                                is_veterinario = is_veterinario)
                user.save()
                persona = Persona.objects.create(nombre = nombre,
                                                      apellido = apellido,
                                                      dni = dni,
                                                      direccion = direccion,
                                                      correo = correo,
                                                      telefono= telefono)
                persona.save()
                cliente =Cliente.objects.create(usuario = user,
                                                datos = persona)
                cliente.save()
                
                return redirect('registrar_primera_mascota', correo)
                return render(request, 'registro/registrar_primer_mascota.html', {'titulo': "Registrar Mascota", 'dueno': cliente.pk, 'form':form} )
        else:
            if not son_todos_letras:
                messages.info(request, MENSAJE_SOLO_LETRAS)
            if not son_todos_numeros:
                messages.info(request, MENSAJE_SOLO_NUMEROS)
            if contraseña !=contraseña_confir:
                messages.info(request, 'Las contraseñas no son las mismas')
            if not correo_existe:
                messages.info(request, 'La direccion de correo electronico no existe')
            return redirect(registro)
            

    else:
        return render(request, 'registro/registro.html')

@login_required   
def registrar_primera_mascota(request, email_de_cliente):
    form = MascotaForm()
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)

        email_de_cliente = request.POST.get('email_de_cliente')

        fecha = request.POST['fecha_nac']
        nombre = request.POST['nombre']
        color = request.POST['color']
        raza = request.POST['raza']

        ingreso_solo_letras = todos_cadenas(nombre, color, raza)
        fecha_es_anterior_a_hoy = fecha_anterior_is_valid(fecha)
        if form.is_valid() and fecha_es_anterior_a_hoy  and ingreso_solo_letras:
            
            mascota = form.save(commit=False)

            if 'foto' in request.FILES:
                mascota.foto = request.FILES['foto']
            mascota.fecha_nac =fecha
            #Aca obtengo el dueño al que pertenece el usuario
            mascota.dueno = Cliente.objects.filter(datos__correo=email_de_cliente)[0] # asignar el valor adicional al campo correspondiente

            mascota.save()
            #Si todo salio bien vuelve al menu principal
            messages.info(request, "Mascota registrada")
            return redirect("main")  

        # Verificar errores y mostrar mensajes personalizados

        if not fecha_es_anterior_a_hoy:
            form.errors['fecha_nac'] = [MENSAJE_FECHA_INVALIDA]

        if not cadena_is_valid(nombre):
            form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]

        if not cadena_is_valid(raza):
            form.errors['raza'] = [MENSAJE_SOLO_LETRAS]
        
        if not cadena_is_valid(color):
            form.errors['color'] = [MENSAJE_SOLO_LETRAS]

        if form.errors:
            for field_name, errors in form.errors.items():
                if (field_name == 'foto'):
                    form.errors['foto'] = ["Imagen invalida, verifique que el archivo sea de tipo .jpg, .png o jpeg"]
                    
    context = {'form':form, 'titulo': "Registro de Mascota", 'email_de_cliente':email_de_cliente}
    return render(request, "registro/registrar_primer_mascota.html", context)
