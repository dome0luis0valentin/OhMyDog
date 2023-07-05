from datetime import date
from django.contrib import messages
from django.shortcuts import render , redirect
from .forms import CampanaForm , PagoForm , PagoFormVisita
from main.models import Campana , User
from django.contrib.auth.decorators import login_required
from validate_email_address import validate_email
from .validaciones import *
from .models import *
from Mensaje import MENSAJE_NO_HAY_DONACIONES
@login_required
def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        
        nombre = request.POST["nombre"]
        motivo = request.POST["motivo"]
        fecha_fin = request.POST["fecha_fin"]
        
        if Campana.objects.filter(nombre=nombre).exists():
            messages.info(request,'Ya Existe una campaña con ese nombre')  
            return redirect('crear_campana')
        
        if form.is_valid() and fecha_is_valid(fecha_fin):
            # Procesar los datos del formulario si es válido
            # Realizar acciones con los datos del formulario (guardar en la base de datos, etc.)
            
            campana = Campana(nombre=nombre, motivo=motivo, fecha_fin=fecha_fin, Total_donado=0.0)

            # Guardar el objeto en la base de datos
            campana.save()
            
            return redirect('main')  
        elif not fecha_is_valid(fecha_fin):
            messages.info(request,'La Fecha tiene que ser mayor a la de hoy')
            return redirect('crear_campana')
    else:
        form = CampanaForm()
    
    return render(request, 'crear_campana.html', {'form': form})

def ver_campanas(request , user_id):
    
    hoy = datetime.now().date()
    # Obtener todas las campañas que no han finalizado
    campanas = Campana.objects.all()
    tipo_usuario="U"
    # Pasar las campañas a la plantilla para su visualización
    context = {'campanas': campanas , 'user_id':user_id , 'fecha_hoy':hoy ,'tipo_usuario':tipo_usuario}
    return render(request, 'ver_campanas.html', context)

from itertools import chain

@login_required
def ver_donacionesa_a_campaña(request, pk):
    # Obtener los QuerySets individuales
    campania = Campana.objects.get(pk= pk)
    queryset1 = Donaciones.objects.filter(campania= campania.nombre)
    queryset2 = DonacionesVisitantes.objects.filter(campania= campania.nombre)

    # Combinar los QuerySets en una única lista
    lista = list(chain(queryset1, queryset2))

    return render(request, "lista_de_donaciones.html", {'lista': lista, 'no_hay': MENSAJE_NO_HAY_DONACIONES})

@login_required
def ver_donaciones(request):
    lista = Campana.objects.all()
    return render(request, "lista_de_campañas.html", {'lista': lista})

def ver_campanas_visitante(request):
    
    hoy = datetime.now().date()
    # Obtener todas las campañas que no han finalizado
    campanas = Campana.objects.all()

    # Pasar las campañas a la plantilla para su visualización
    context = {'campanas': campanas ,'fecha_hoy':hoy, 'tipo':"V" }
    return render(request, 'ver_campanas.html', context)

@login_required
def ver_mis_donaciones(request): 
    donaciones = Donaciones.objects.filter(usuario__email = request.user.email)

    # Pasar las campañas a la plantilla para su visualización
    context = {'donaciones': donaciones}
    return render(request, 'ver_mis_donaciones.html', context)

def formulario_pago(request , campana_id , user_id):
    form = PagoForm(request.POST)
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            
            numero_de_tarjeta = request.POST["numero_de_tarjeta"]
            cantidad = request.POST["cantidad"] 
            
            cantidad = float(request.POST["cantidad"])
            campana = Campana.objects.get(id=campana_id)
            # Actualiza el campo Total_donado
            campana.Total_donado += cantidad
            # Guarda los cambios en la base de datos
            campana.save()
            
            if int(cantidad) <= 0:
                messages.info(request,"la cantidad a abonar tiene que ser mayor a 0 ")    
                return redirect('formulario_pago',campana_id=campana_id, user_id=user_id)   
            
            estado_pago = proceso_pago(numero_de_tarjeta,cantidad)
            
            if not estado_pago[0] :
                messages.info(request,estado_pago[1])    
                return redirect('formulario_pago',campana_id=campana_id, user_id=user_id)
                
            user = User.objects.get(id=user_id)
            user.descuento+=cacular_descuento(cantidad)
            user.save()
            
            #crear un modelo donacion con campana_id , usuario_id y monto donado ; y guardar esos datos
            
            donacion = Donaciones(campania=campana.nombre,usuario=user, monto=cantidad)
            donacion.save()
            
            
            return render(request, 'confirmacion.html')
    return render(request, 'donar.html', {'form': form , 'user_id':user_id , 'tipo':"U"})

#usuario visitante 
def formulario_pago_visitante(request , campana_id ):
    form = PagoFormVisita(request.POST)
    if request.method == 'POST':
        form = PagoFormVisita(request.POST)
        if form.is_valid():
            
            numero_de_tarjeta = request.POST["numero_de_tarjeta"]
            cantidad = request.POST["cantidad"]
            correo = request.POST["correo"] 
            
            cantidad = float(request.POST["cantidad"])
            campana = Campana.objects.get(id=campana_id)
            # Actualiza el campo Total_donado
            campana.Total_donado += cantidad
            # Guarda los cambios en la base de datos
            campana.save()
            
            #correo_existe = (True == validate_email(correo, verify=True))
            
            estado_pago = proceso_pago(numero_de_tarjeta,cantidad)
            
            if not estado_pago[0] :
                messages.info(request,estado_pago[1])    
                return redirect('formulario_pago_visitante',campana_id=campana_id)
            
            if len(correo) < 15:
                messages.info(request,"El correo ingresado es inavalido o no existe")    
                return redirect('formulario_pago_visitante',campana_id=campana_id)            
            #crear un modelo donacion con campana_id , usuario_id y monto donado ; y guardar esos datos
            
            donacion = DonacionesVisitantes(campania=campana.nombre,correo=correo, monto=cantidad)
            donacion.save()
            
            
            return render(request, 'confirmacion.html')
    return render(request, 'donar.html', {'form': form , 'tipo':"V"})