from typing import Any
from django.views import generic
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta

from django.core.paginator import Paginator

from datetime import datetime

from .models import Mascota,Intentos,Visitas, Cliente, Mascota_Adopcion, Red_Social, Turno, Prestador_Servicios, Vacuna_tipoA , Vacuna_tipoB
from .form import UrgenciaForm,UsuarioForm,FormularioAdopcionForm, MascotaAdopcionForm,Red_SocialForm , MascotaForm, TurnoForm, ServicioForm
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


from .form import CustomPasswordChangeForm


def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(10))
    return contrasena

def mascota_repetida(nombre, email):
    return Mascota.objects.filter(nombre=nombre, dueno__usuario__email=email).exists()

def enviar_nueva_contraseña(user, asunto):
    remitente = 'grupo21ing2@gmail.com'  # Dirección de correo electrónico del remitente
    nueva_contraseña = generar_contrasena()
    mensaje = "Esta es tu nueva contraseña: "+nueva_contraseña  # Contenido del mensaje

    email = EmailMessage(asunto, mensaje, to=[user])
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
        try:
            numero = int(cadena)
            if numero <= 0:
                return False
        except ValueError:
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

MENSAJE_USARIO_YA_EXISTE = 'Este correo electrónico ya se encuentra ocupado por otro usuario, si desea continuar con el registro, cambie el correo'
MENSAJE_FECHA_POSTERIOR = 'Fecha invalida NO debe ser una fecha posterior a la de hoy'
MENSAJE_FECHA_ANTERIOR = 'Fecha invalida debe ser una fecha posterior a la de hoy'
MENSAJE_FECHA_INVALIDA = 'Verifique que la fecha tenga el formato DD/MM/AAAA y que sea un dia valido. Ejemplo: 01/01/2023'
MENSAJE_USUARIO_INVALIDO = 'Usuario incorrecto, revise que el email sea correcto y que el cliente este registrado'
MENSAJE_SOLO_LETRAS = 'Solo se permiten letras, no ingrese numeros, ni simbolos como #,$,/, etc.'
MENSAJE_SOLO_NUMEROS = "Solo se permiten números, no ingrese simbolos como .,-, /, etc."
MENSAJE_MASCOTA_REPETIDA = "Ya tiene una mascota registrada con este nombre, si desea continuar con el registro, cambie el nombre de la mascota"

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
                        usuario.set_password(enviar_nueva_contraseña(nombre_usuario, "Desbloquer usuario"))
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
    return redirect('/')

def usuario_bloqueado(request):
    return render(request, 'usuario_bloqueado.html')

def cambiar_contraseña(request):
    if request.method == 'POST':
       
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Actualiza la sesión del usuario.
            update_session_auth_hash(request, user)  
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)
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
    lista = Mascota.objects.all()
    num_mascotas = Mascota.objects.filter(dueno__usuario__email = auth.user.email)
    main_data = {"lista": lista}
    return render(request, "lista_mascota.html", {"cantidad": num_mascotas, "lista":lista})
   
#Mostar detalle de mascota
def detalle_mascota(request, pk=None):
    return render(request, "prueba_detalle_mascota.html")   

def confirmar_eliminar_mascota(request, mascota_id):
    return render(request,'mis_mascotas/confirmar_eliminar.html', {'id': mascota_id, 'accion': "eliminar mascota"})

def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    messages.success(request, f'Se ha dado de baja a : "{mascota.nombre}" ')
    turnos_de_mascota = Turno.objects.filter(mascota=mascota)
    
    turnos_de_mascota.delete()
    visitas_mascota = Visitas.objects.filter(mascota=mascota)
    visitas_mascota.delete()
    mascota.delete()
    return redirect('Ver mis Mascotas')    

def marcar_adopcion(request, pk):
    perro = get_object_or_404(Mascota_Adopcion, pk=pk)
    perro.estado = 'a'
    perro.save()
    return redirect('ver mis adopciones')


def formulario_adopcion(request):
    print("Por lo menos estoy aca")
    if request.method == 'POST':
        form = FormularioAdopcionForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre = cleaned_data['nombre']
            apellido = cleaned_data['apellido']
            dni = cleaned_data['dni']
            correo = cleaned_data['correo']
            telefono = cleaned_data['telefono']
            motivo = cleaned_data['motivo']

            ingreso_solo_letras = todos_cadenas(nombre, apellido)
            ingreso_solo_numeros = todos_numeros(telefono, dni)
            correo_existe = validate_email(correo, verify=True)

            if ingreso_solo_letras and ingreso_solo_numeros and correo_existe:
                # Renderizar la plantilla de correo electrónico
                html_message = render_to_string('email_template.html', {'nombre': nombre, 'apellido': apellido, 'dni': dni, 'correo': correo, 'telefono': telefono, 'motivo': motivo})
                plain_message = strip_tags(html_message)

                # Enviar el correo electrónico
                send_mail(
                    'Formulario de adopción',
                    plain_message,
                    correo,
                    ['grupo21ing2@gmail.com'],
                    html_message=html_message,
                )

                messages.success(request, "Solicitud enviada")
                return redirect('adopciones')
            else:
                if not ingreso_solo_letras:
                    messages.info(request, "El nombre y apellido deben contener solo letras")
                if not ingreso_solo_numeros:
                    messages.info(request, "El DNI y teléfono deben contener solo números")
                if not correo_existe:
                    messages.info(request, "La dirección de correo electrónico no existe")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.info(request, f"Error en el campo {field}: {error}")

        return redirect('adopciones')

    else:
        initial_data = {}
        if request.user.is_authenticated:
                cliente = Cliente.objects.get(usuario__email=request.user.email)
                cliente = cliente.datos
                nombre = cliente.nombre
                apellido = cliente.apellido
                dni = cliente.dni
                correo = request.user.email
                telefono = cliente.telefono
                initial_data = {'nombre': cliente.nombre,
                                'apellido': cliente.apellido,
                                'dni': cliente.dni,
                                'correo' :cliente.correo,
                                'telefono' : cliente.telefono}        
        form = FormularioAdopcionForm(initial=initial_data)

        return render(request, "formulario_adopcion_auto.html", {'form': form})



def enviar_formulario_adopcion(request):
    if request.method == 'POST':

        if (request.user.is_authenticated):
            cliente = Cliente.objects.filter(usuario__email=request.user.email)[0]
            nombre = cliente.datos.nombre
            apellido = cliente.datos.apellido
            dni = cliente.datos.dni
            correo = request.user.email
            telefono = cliente.datos.telefono
        else:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            dni = request.POST.get('dni')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')

        motivo = request.POST.get('motivo')

        ingreso_solo_letras = todos_cadenas(nombre, apellido)
        ingreso_solo_numeros = todos_numeros(telefono, dni)

        correo_existe = (True == validate_email(correo, verify=True)) 

        
        if (ingreso_solo_letras and ingreso_solo_numeros and correo_existe):
            # Renderizar la plantilla de correo electrónico
            html_message = render_to_string('email_template.html', {'nombre': nombre, 'apellido': apellido, 'dni': dni, 'correo': correo, 'telefono': telefono, 'motivo': motivo})
            plain_message = strip_tags(html_message)

            # Enviar el correo electrónico
            send_mail(
                'Formulario de adopción',
                plain_message,
                correo,
                # tendriamos que agregar el gmail del usuario que publico la adopcion mejor dicho el dueño del perro
                ['grupo21ing2@gmail.com'],
                html_message=html_message,
            )
            
            messages.success(request, "Solicitud Enviada")
            # Redireccionar a una página de éxito
            return redirect('adopciones')
        else:
            if not cadena_is_valid(nombre):
                messages.info(request, "El nombre ingresado no es valido, "+MENSAJE_SOLO_LETRAS)
            if not cadena_is_valid(apellido):
                messages.info(request,"El apellido ingresado no es valido, "+ MENSAJE_SOLO_LETRAS)
            if not numero_is_valid(dni):
                messages.info(request, "El DNI ingresado no es valido, "+MENSAJE_SOLO_NUMEROS)
            if not numero_is_valid(telefono):
                messages.info(request, "El Telefono ingresado no es valido, "+MENSAJE_SOLO_NUMEROS) 
            if not correo_existe:
                messages.info(request, 'La direccion de correo electronico no existe')
            
            return redirect('adopciones')
    else:
        
        return render(request, 'formulario_adopcion.html') 
    

#-----------------------------SECCION DE LISTAS-------------------------------------


class AdopcionListView(generic.ListView):
    
    model = Mascota_Adopcion 

    context_object_name = 'lista_mascotas_adopcion'   # your own name for the list as a template variable
    #queryset = Mascota_Adopcion.objects.filter(dueno__usuario__email != request.user.email) #Metodo que devuelve las mascotas, se puede poner un filter
    template_name = 'adopcion/lista_mascotas_adopcion.html'  # Specify your own template name/location

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_email = self.request.user.email
            queryset = super().get_queryset()
            queryset = queryset.exclude(dueno__usuario__email=user_email)
        else:
            queryset = Mascota_Adopcion.objects.all()    
            
        return queryset

class MascotaListView(LoginRequiredMixin, generic.ListView):
    model = Mascota # Modelo al que le va a consultar los datos

    context_object_name = 'lista_mascotas'   # your own name for the list as a template variable

    def get_queryset(self):
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
    
from django.shortcuts import get_object_or_404

def servicio_detail_view(request, pk):
    servicio = get_object_or_404(Prestador_Servicios, pk=pk)
    red_social = get_object_or_404(Red_Social, dueno__pk=pk)

    return render(
        request,
        'servicios/detalle.html',
        context={'servicio': servicio, 'red_social': red_social}
    )

class ServicioDetailView(generic.DetailView):
    model = Prestador_Servicios
    template_name = 'servicios/detalle.html'  

    def servicio_detail_view(request,pk):
        try:
            red_social = Red_Social.objects.get(pk=0)
            servicio_id=Prestador_Servicios.objects.get(pk=pk)

        except Prestador_Servicios.DoesNotExist:
            print("Error")
            raise Http404("Este servicio no esta registrado")
        
        return render(
            request,
            'main/templates/servicios/detalle.html',
            context={'servicio':servicio_id, 'red_social':red_social}
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
                form.errors['fecha_nac'] = [MENSAJE_FECHA_POSTERIOR]

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
        zona = request.POST['zona']
        nombre_red = request.POST['nombre_red']

        son_todos_cadenas = todos_cadenas(nombre, apellido, nombre_red)
        son_todos_numeros = todos_numeros(telefono, dni)

        correo_existe = (True == validate_email(correo, verify=True)) 


        if form.is_valid() and red_form.is_valid() and son_todos_cadenas and son_todos_numeros and correo_existe:
        
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
                                                                            tipo = tipo,
                                                                            zona = zona)
                prestador_de_servicios.save()
                
                red.dueno = prestador_de_servicios

                red.save()
                messages.success(request,"Se registro el servicio")
                return redirect('main')

                print("\nSe registro un servicio")
            else:
                form.errors['correo'] = ["El usuario ya existe"]
                form.errors['zona'] = ["Zona incorrecta, debe ser una valor entre 1 y 25"]
        else:
             # Verificar errores y mostrar mensajes personalizados

            if not cadena_is_valid(nombre):
                form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]
            
            if not cadena_is_valid(apellido):
                form.errors['apellido'] = [MENSAJE_SOLO_LETRAS]

            if not cadena_is_valid(nombre_red):
                red_form.errors['nombre_red'] = [MENSAJE_SOLO_LETRAS]

            if not numero_is_valid(dni):
                form.errors['dni'] = [MENSAJE_SOLO_NUMEROS]
            
            if not numero_is_valid(telefono):
                form.errors['telefono'] = [MENSAJE_SOLO_NUMEROS]

            if not numero_is_valid(telefono):
                form.errors['correo'] = ["El correo ingresado no existe"]
            
    
    context = {'form':form,'red_form': red_form, 'titulo': "Registro de Servicios de Terceros"}

    return render(request, "registro_servicio.html", context)


@login_required
def registrar_urgencia(request):
    form = UrgenciaForm()
   
    if request.method == "POST":
        form = UrgenciaForm(request.POST) 

        banda_horaria = request.POST['banda_horaria']
        fecha = request.POST['fecha']
        motivo = 'U'
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
        repetida = mascota_repetida(nombre, request.user.email)

        if form.is_valid() and fecha_es_anterior_a_hoy  and ingreso_solo_letras and not(repetida):
            
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
            form.errors['fecha_nac'] = [MENSAJE_FECHA_POSTERIOR]

        if not cadena_is_valid(nombre):
            form.errors['nombre'] = [MENSAJE_SOLO_LETRAS]

        if not cadena_is_valid(raza):
            form.errors['raza'] = [MENSAJE_SOLO_LETRAS]
        
        if not cadena_is_valid(color):
            form.errors['color'] = [MENSAJE_SOLO_LETRAS]

        if repetida:
            form.errors['nombre']= [MENSAJE_MASCOTA_REPETIDA]

        if form.errors:
            for field_name, errors in form.errors.items():
                if (field_name == 'foto'):
                    form.errors['foto'] = ["Imagen invalida, verifique que el archivo sea de tipo .jpg, .png o jpeg"]
                    
    context = {'form':form, 'titulo': "Registro de Mascota"}
    return render(request, "registro.html", context)

def mascota_cumple(mascota,fecha,fecha_nac,tipo):
    
    fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
    edad_meses = int((fecha_ingresada - fecha_nac).days / 30)

    print(edad_meses, tipo)
    
    if tipo == "Vacunación de tipo A" :
        
        if Vacuna_tipoA.objects.filter(mascota_id = mascota.id).exists() :
            
            vacuna = Vacuna_tipoA.objects.get(mascota_id = mascota.id) 
                      
            if edad_meses > 2 and edad_meses < 4 :
                return [fecha_ingresada > (vacuna.fecha_aplicacion + timedelta(days=21)),"No se puede aplicar la vacuna por que no an pasado los 21 dias de espera"]
            elif edad_meses > 4 :
                return [fecha_ingresada > (vacuna.fecha_aplicacion + relativedelta(years=1)),"No se puede aplicar la vacuna por que no an pasado el año de espera"]
        else:  
              if edad_meses < 2 :
                  return [False,"La mascota es muy pequeña para aplicarle la vacuna tipo A"]
              else: 
                  return[True,""]
                      
    elif tipo == "Vacunación de tipo B":
        if Vacuna_tipoB.objects.filter(mascota_id = mascota.id).exists() :
            
            vacuna = Vacuna_tipoB.objects.get(mascota_id = mascota.id)           
            if edad_meses > 4 :
                return [fecha_ingresada > vacuna.fecha_aplicacion + relativedelta(years=1),"No se puede aplicar la vacuna por que no a pasado el año de espera"] 
        else: 
            if edad_meses < 4:
                return [False,"La mascota no tiene todavia mas de 4 meses de edad , para aplicarle la vacuna tipo B"]
            else:
               return[True,""] 
    
    if (tipo != "A" and tipo != "B"):
        return [True,""]      


@login_required
def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        dni = request.POST['dni']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        is_veterinario = request.POST.get('is_veterinario', False)
        
        is_veterinario = (is_veterinario=='on')
       
        son_todos_letras = todos_cadenas(nombre, apellido)
        son_todos_numeros = todos_numeros(telefono, dni)

        
        correo_existe = (True == validate_email(correo, verify=True)) 

        if son_todos_numeros and son_todos_letras and correo_existe:
            if User.objects.filter(username=correo).exists():
                messages.info(request, MENSAJE_USARIO_YA_EXISTE)
                return redirect(registro)
            elif User.objects.filter(email=correo).exists():
                messages.info(request, MENSAJE_USARIO_YA_EXISTE)
                return redirect(registro)
            else:

                contraseña = enviar_nueva_contraseña(correo, "Contraseña para OhMyDog!")
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
        else:
            if not son_todos_letras:
                messages.info(request, MENSAJE_SOLO_LETRAS)
            if not son_todos_numeros:
                messages.info(request, MENSAJE_SOLO_NUMEROS)
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
