from main.models import Mascota, Cliente,Turno, Prestador_Servicios, Persona , Vacuna_tipoA ,Vacuna_tipoB, Visitas
from .models import Veterinarias_de_turno
from main.form import Red_SocialForm , TurnoForm, ServicioForm
from .forms import VeterinariasForm , FormularioSimple , DesparasitanteForm ,VacunacionForm
from django.urls import reverse
from Campania.models import Donaciones
from django.db.models import Q


from datetime import datetime , timedelta , date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Funciones import *
from Mensaje import *
from validate_email_address import validate_email
from django.views import generic
from .validaciones import archivo_is_valid, mascota_cumple , descuento

from django.contrib.auth.mixins import LoginRequiredMixin

import csv 
    
from .funciones import *
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
        print("Mascota que solicita el turno", mascota)
        motivo = request.POST["motivo"]

        fecha_nacimineto = mascota.fecha_nac

        resultado_mascota_cumple = mascota_cumple(mascota,fecha,fecha_nacimineto,motivo)

        #Python no valida todo el condicional, si el form no es valido no valida la fecha
        if form.is_valid() and fecha_is_valid(fecha) and resultado_mascota_cumple[0]:
            
            # tengo que validar que el cliente  no tenga un turno para la mascota con el mismo motivo 
            if Turno.objects.filter(cliente=cliente, mascota=mascota , motivo=motivo , estado="E").exists() or Turno.objects.filter(cliente=cliente, mascota=mascota , motivo=motivo , estado="A").exists():
                if Visitas.objects.filter(cliente=cliente, mascota=mascota , motivo="Castración").exists():
                    messages.error(request, "La mascota ya fue castrada")
                else:    
                    messages.error(request, "Ya has solicitado un turno  para la mascota")
                    messages.error(request, "Podras solicitar de nuevo un turno cuando finalise el turno solicitado o sea rechasado")
                return redirect('solicitar turno')
    
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
                    messages.info(request, MENSAJE_FECHA_INVALIDA)
                else:    
                    messages.info(request, MENSAJE_FECHA_ANTERIOR)
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
def turno_confirmado_detail_view(request, pk,tipo):
    turno = get_object_or_404(Turno, pk=pk)
    print(turno.mascota)
    mascota = get_object_or_404(Mascota, pk=turno.mascota.id)

    return render(
        request,
        'detalle_turnos_aceptados.html',
        context={'object': turno, 'mascota': mascota , 'tipo':tipo}
    )    
    
@login_required
def rechazar_turno(request, turno_id):
    if request.method == 'POST':
        #rechazar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='R'
        turno.save()

        return redirect('confirmar_turnos')
        
@login_required
def aceptar_turno(request, turno_id):
    if request.method == 'POST':
        #aceptar
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='A'
        turno.save()

        return redirect('confirmar_turnos')    

@login_required
def turnos_confirmados(request):
    fecha_actual = date.today()
    turnos_confirmados_fecha = Turno.objects.filter(fecha=fecha_actual, estado="A")
    contexto = {'turnos_confirmados': turnos_confirmados_fecha , 'tipo' : "C"}
    return render(request, "lista_de_turnos_aceptados.html", contexto)  


@login_required
def turnos_solo_confirmados(request):
    turnos_confirmados = Turno.objects.filter(estado="A") 
    contexto = {'turnos_confirmados': turnos_confirmados , 'tipo' : "S"}
    return render(request, "lista_de_turnos_aceptados.html", contexto )  
    
@login_required    
def Falto_al_turno(request, turno_id):
    if request.method == 'POST':
        #falto al turno 
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='F'
        turno.save()

        return redirect('turnos_confirmados')    

@login_required 
#ya no es necesario   
def Asistio_al_turno(request, turno_id):
    if request.method == 'POST':
        #aceptar
        turno = Turno.objects.filter(id = turno_id)[0]
        print("_____________________________")
        print(request.method)
        url = reverse(turno.motivo,{'turno_id': turno_id})
        return redirect(url)

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

 
def ver_veterinarias_de_turno(request):

    if(Veterinarias_de_turno.objects.exists()):
        #Mostrar Veterinarias
        ultimo_subido = Veterinarias_de_turno.objects.last().arch
        
        data = leer_archivo(ultimo_subido.name)
        return render(request, 'mostrar_veterinarias_de_turno.html', {'data': data})
    else:
        #Mostrar error
        messages.error(request, MENSAJE_NO_HAY_VETERINARIAS)
        return redirect("main")

@login_required   
def ver_historial_de_turnos(request):

    usuarios = Turno.objects.filter(cliente__usuario__email=request.user.email)
    #Tiene turnos
    if(usuarios.exists()):
        data = Turno.objects.filter(mascota__dueno__usuario__email=request.user.email) 
        
    #No tiene turnos
    else:
        data = []

    return render(request, 'historial/turnos_solicitados.html', {'data': data})

@login_required   
def ver_historial_de_visitas(request, pk):

    visitas = Visitas.objects.filter(mascota__pk=pk)
    #Tiene visitas
    if(visitas.exists()):
        data = visitas  
    #No tiene visitas
    else:
        data = []

    return render(request, 'historial/visitas.html', {'data': data})

@login_required   
def ver_libreta_sanitaria(request, pk):

    libreta = Visitas.objects.filter(
        Q(mascota__pk=pk) &
        (Q(motivo='Vacunación de tipo A') | Q(motivo='Vacunación de tipo B') | Q(motivo='Desparasitación'))
    )

    for i in libreta:
        print(i)
        print(i.peso)
        print(i.cant_desparacitante)
        print(i.codigo)

    #Tiene visitas
    if(libreta.exists()):
        data = libreta  
    #No tiene visitas
    else:
        data = []

    return render(request, 'historial/historial_turnos.html', {'data': data})

@login_required
def formulario_simple(request, turno_id):
    print("Entro a simple")
    print(request.method)
    if request.method == 'POST':
        print("Entro a post")
        form = FormularioSimple(request.POST)
        
        if form.is_valid():
            descripcion = request.POST["descripcion"]
            monto = request.POST["monto"]
            turno = Turno.objects.filter(id = turno_id)[0]
            print("Registro")
           
            registrar_visita_simple(descripcion, monto, turno)

            return redirect('actualizar_turno', turno_id=turno_id, monto=str(monto))
        else:
            return render(request, 'formularios/formulario_simple.html', {'form': form, 'turno_id': turno_id})
    else:
        form = FormularioSimple(request.POST)
    return render(request, 'formularios/formulario_simple.html', {'form': form, 'turno_id': turno_id})

@login_required
def formulario_desparasitante(request, turno_id):
    if request.method == 'POST':
        form = DesparasitanteForm(request.POST)
        peso = request.POST["peso"]

        if form.is_valid() and es_numero_real_positivo(peso):
            turno = Turno.objects.get(id = turno_id)

            registrar_visita_desparacitacion(turno, request)
            messages.info(request,"Desparasitación registrada")
            monto =  str(request.POST["monto"])
            return redirect('actualizar_turno',turno_id=turno_id, monto=monto)  
        else: 
            form.errors["peso"]=["El peso tiene que ser positivo"]
            return render(request, 'formularios/formulario_desparacitante.html', {'form': form, 'turno_id': turno_id})
    else:
        form = DesparasitanteForm()
        return render(request, 'formularios/formulario_desparacitante.html', {'form': form, 'turno_id': turno_id})
    
@login_required
def formulario_vacunacion(request, turno_id):
    print("Entro a Vacunacion")
    if request.method == 'POST':
        form = VacunacionForm(request.POST)
        if form.is_valid():
            print("Formulario valido")
            turno = Turno.objects.filter(id = turno_id)[0]
            registrar_visita_vacunacion(turno, request)
            acturalizar_modelos(turno)
            messages.info(request,"Vacunación registrada")
            monto =  str(request.POST["monto"])
            return redirect('actualizar_turno', turno_id=turno_id, monto=monto)
        else:
            return render(request, 'formularios/formulario_vacunacion.html', {'form': form, 'turno_id': turno_id})   
    else:
        form = VacunacionForm()    
    return render(request, 'formularios/formulario_vacunacion.html', {'form': form, 'turno_id': turno_id})

def acturalizar_modelos(turno):
    print("Se actualizo la vacunacion")
    if (turno.motivo =="Vacunación de tipo A"):
        aplicacion_vacuna = Vacuna_tipoA.objects.create(mascota=turno.mascota, fecha_aplicacion=turno.fecha)
    else:
        aplicacion_vacuna = Vacuna_tipoB.objects.create(mascota=turno.mascota, fecha_aplicacion=turno.fecha)
    aplicacion_vacuna.save()          


@login_required
def actualizar_turno(request, turno_id, monto):
    print(request.method, "Actualizando turno")
    if True:
        turno = Turno.objects.filter(id = turno_id)[0]
        
        info_turno=Turno.objects.get(id=turno_id)
        cliente_id = info_turno.cliente_id
        cliente = Cliente.objects.get(id = cliente_id)
        usuario_id = cliente.usuario_id
        usuario = User.objects.get(id = usuario_id)

        turno.estado='As'
        turno.save()
        #aca se tiene que guardar el turno en la visita y en la libreta sanitaria 
        
        mascota= Mascota.objects.get(id = info_turno.mascota_id)
        
        donaciones=Donaciones.objects.filter(usuario_id=usuario_id)
        nombres_campanias = [donacion.campania for donacion in donaciones]
        monto_de_cada_campania = [donacion.monto for donacion in donaciones]
        lista_descuentos = [cacular_descuento(int(donacion.monto)) for donacion in donaciones]
        donaciones_usuario= zip(nombres_campanias,monto_de_cada_campania,lista_descuentos)
        donaciones.delete()

        
        context= {'servicio':info_turno.motivo , 'fecha_turno': info_turno.fecha , 'banda_horaria': info_turno.banda_horaria , 
                  'mascota' : mascota.nombre , 'total_a_pagar':descuento(monto,usuario.descuento) , 
                  'descuento':usuario.descuento , 'monto_a_cobrar':monto , 'donaciones_usuario':donaciones_usuario}
        
        usuario.descuento = 0
        
        usuario.save()
        
        return render(request, 'factura.html' , context)
    else:                  
        return redirect('turnos_confirmados') 

def calcelar_turno(request, turno_id):
    if request.method == 'POST':
        turno = Turno.objects.filter(id = turno_id)[0]
        turno.estado='Ca'
        turno.save()
        messages.info(request,"Registro cancelado")
    return redirect('main')          
