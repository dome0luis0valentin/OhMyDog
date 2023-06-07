from datetime import date
from django.shortcuts import render , redirect
from .forms import CampanaForm , PagoFrom
from main.models import Campana , User
from django.contrib.auth.decorators import login_required
from .validaciones import *

@login_required
def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        
        nombre = request.POST["nombre"]
        motivo = request.POST["motivo"]
        fecha_fin = request.POST["fecha_fin"]
        
        if Campana.objects.filter(nombre=nombre).exists():
            return redirect('crear_campana')
        
        if form.is_valid() and fecha_is_valid(fecha_fin):
            # Procesar los datos del formulario si es válido
            # Realizar acciones con los datos del formulario (guardar en la base de datos, etc.)
            
            campana = Campana(nombre=nombre, motivo=motivo, fecha_fin=fecha_fin, Total_donado=0.0)

            # Guardar el objeto en la base de datos
            campana.save()
            
            return redirect('main')
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
    form = PagoFrom(request.POST)
    if request.method == 'POST':
        form = PagoFrom(request.POST)
        if form.is_valid():
            
            cantidad = float(request.POST["cantidad"])
            campana = Campana.objects.get(id=campana_id)
            # Actualiza el campo Total_donado
            campana.Total_donado += cantidad
            # Guarda los cambios en la base de datos
            campana.save()
            
            user = User.objects.get(id=user_id)
            user.descuento+=cacular_descuento(cantidad)
            user.save()
            
            return render(request, 'confirmacion.html')
    return render(request, 'donar.html', {'form': form , 'user_id':user_id})