from datetime import datetime
import random

def fecha_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada >= hoy
    except:
        # El usuario no existe en la base de datos
        return False
    
def cacular_descuento(monto):
    return round(monto * 0.20 ) 

def proceso_pago(numero_tarjeta,monto):
    conexionBanco = random.choice([True, False])
    tarjetas_validas=[(1234567890123456,10000),(1234567890987654,0)]
    if conexionBanco:
        for tarjeta in tarjetas_validas:
            numeor = int(tarjeta[0])
            saldo = int(tarjeta[1])
            if numeor == int(numero_tarjeta):
                if ((saldo - int(monto)) > int(monto)): 
                    return[True,"Tiene saldo suficiente"]
                else:
                    return[False,"No tiene saldo suficiente"]
        return[False,"El numero de tarjeta es incorrecto"]     
    else:
        return[False,"No tenemos conexion con el banco"]
