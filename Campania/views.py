from datetime import date
from django.contrib import messages
from django.shortcuts import render , redirect
from .forms import CampanaForm , PagoForm
from main.models import Campana , User
from django.contrib.auth.decorators import login_required
from .validaciones import *
from .models import *

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
    # Obtener todas las campañas que no han finalizado
    campanas = Campana.objects.all()

    # Pasar las campañas a la plantilla para su visualización
    context = {'campanas': campanas , 'user_id':user_id}
    return render(request, 'ver_campanas.html', context)

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
    return render(request, 'donar.html', {'form': form , 'user_id':user_id})