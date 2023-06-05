from datetime import datetime

def fecha_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada >= hoy
    except:
        # El usuario no existe en la base de datos
        return False