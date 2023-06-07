from datetime import datetime
from main.models import Mascota, Cliente
from .models import MascotasPerdidas
def fecha_anterior_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada <= hoy
    except:
        return False
    
def mascota_perdida(id):
    return Mascota.objects.get(id=id).perdida

def validar_existencia(email, nombre):

    cliente_id = Cliente.objects.get(usuario__email = email)
    if MascotasPerdidas.objects.filter(cliente_id=cliente_id, nombre=nombre).exists():
        lista_reg = MascotasPerdidas.objects.filter(cliente_id=cliente_id, nombre=nombre)
        for mascota_registra in lista_reg:
            if (mascota_registra.encontrado == False):
                return True
    return False
    