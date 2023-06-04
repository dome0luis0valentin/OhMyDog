from datetime import datetime
def fecha_anterior_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada <= hoy
    except:
        return False
    