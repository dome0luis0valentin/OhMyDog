from main.models import Mascota, Cliente,Turno, Prestador_Servicios, Vacuna_tipoA , Vacuna_tipoB , Persona
from main.form import UrgenciaForm,Red_SocialForm , TurnoForm, ServicioForm
from .forms import VeterinariasForm
from datetime import datetime 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Funciones import *
from Mensaje import *
from validate_email_address import validate_email
from django.views import generic
from .validaciones import archivo_is_valid, mascota_cumple
      
    
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

        fecha_nacimineto = mascota.fecha_nac

        resultado_mascota_cumple = mascota_cumple(mascota,fecha,fecha_nacimineto,motivo)
        print(resultado_mascota_cumple)

        #Python no valida todo el condicional, si el form no es valido no valida la fecha
        if form.is_valid() and fecha_is_valid(fecha) and resultado_mascota_cumple[0]:

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
            messages.success(request, "Se registro el turno")
            return redirect("main")
        else:
            if not (fecha_is_valid(fecha)):
                if not fecha_anterior_is_valid(fecha):
                    messages.info(request, MENSAJE_FECHA_ANTERIOR)
                else:    
                    messages.info(request, MENSAJE_FECHA_INVALIDA)
            else:
                messages.info(request,resultado_mascota_cumple[1])    
            
            return redirect('solicitar turno')
        
    context = {'form':form, 'titulo': "Solicitud de Turno"}

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
    template_name = 'lista_de_turnos_pendientes.html'
    
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
def turno_detail_view(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    print(turno.mascota)
    mascota = get_object_or_404(Mascota, pk=turno.mascota.id)

    return render(
        request,
        'detalle.html',
        context={'object': turno, 'mascota': mascota}
    )
    
@login_required
def rechazar_turno(request, turno_id):
    if request.method == 'POST':
        #rechazar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='A'
        turno.save()

        return redirect('confirmar turnos')
        
@login_required
def aceptar_turno(request, turno_id):
    if request.method == 'POST':
        #aceptar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='R'
        turno.save()

        return redirect('confirmar turnos')    

@login_required
def turnos_confirmados(request):
    fecha_actual = datetime.date.today()
    fecha_formateada_actual = fecha_actual.strftime("%YYYY/%mm/%dd")
    turnos_confirmados = Turno.objects.filter(estado ='A',fecha=fecha_formateada_actual)
    contexto = {'turnos_confirmados': turnos_confirmados}
    return render(request, "lista_de_turnos_aceptados.html", contexto)    
    

@login_required
def cargar_veterinarias(request):

    form = VeterinariasForm()

    if request.method == 'POST':
        form = VeterinariasForm(request.POST, request.FILES)
        archivo = request.FILES['arch']
        if form.is_valid() and archivo_is_valid(archivo):
            #Cargar archivo
            veterinarias_de_turno = form.save(commit=False)
            veterinarias_de_turno.fecha_creación = datetime.today()
            veterinarias_de_turno.save()
            messages.success(request, "Archivo cargado con exito")
            return redirect('main')
        else: 
            #Mensaje  de error
            messages.error(request, MENSAJE_ARCHIVO_TURNOS)
            return redirect('cargar veterinarias de turno')
    else:
        context = {'form':form, 'titulo': "Cargar Veterinarias de Turno"}
        return render(request, "cargar_veterinarias.html", context)

            

    

