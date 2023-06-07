from datetime import datetime
from main.models import Mascota
def fecha_anterior_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada <= hoy
    except:
        return False
    
def mascota_perdida(id):
    return Mascota.objects.get(id=id).perdida
    