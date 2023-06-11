import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
from main.models import  Vacuna_tipoA , Vacuna_tipoB 
from dateutil.relativedelta import relativedelta


def archivo_is_valid(archivo):
    extension = archivo.name.split('.')[-1].lower()

    if extension == 'csv':
        df = pd.read_csv(archivo)
    elif extension == 'xlsx' or extension =='xls':
        df = pd.read_excel(archivo)
    else:
        return False
    
    if len(df.columns) < 2:
        return False
    
    primera_columna = df.iloc[:, 0]
    segunda_columna = df.iloc[:, 1]

    if primera_columna.dtype != 'object':
        return False
    
    for fecha in segunda_columna:
        if isinstance(fecha, pd.Timestamp):
            fecha = fecha.strftime('%d/%m/%Y')
        try:
            
            dt.datetime.strptime(fecha, '%d/%m/%Y')

        except ValueError:
            return False
    
    return True

def mascota_cumple(mascota,fecha,fecha_nac,tipo):
    
    fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
    edad_meses = int((fecha_ingresada - fecha_nac).days / 30)

    print(edad_meses, tipo)
    
    if tipo == "Vacunación de tipo A" :
        
        if Vacuna_tipoA.objects.filter(mascota_id = mascota.id).exists() :
            
            vacuna = Vacuna_tipoA.objects.get(mascota_id = mascota.id) 
                      
            if edad_meses > 2 and edad_meses < 4 :
                return [fecha_ingresada > (vacuna.fecha_aplicacion + timedelta(days=21)),"No se puede aplicar la vacuna por que no an pasado los 21 dias de espera"]
            elif edad_meses > 4 :
                return [fecha_ingresada > (vacuna.fecha_aplicacion + relativedelta(years=1)),"No se puede aplicar la vacuna por que no an pasado el año de espera"]
        else:  
              if edad_meses < 2 :
                  return [False,"La mascota es muy pequeña para aplicarle la vacuna tipo A"]
              else: 
                  return[True,""]
                      
    elif tipo == "Vacunación de tipo B":
        if Vacuna_tipoB.objects.filter(mascota_id = mascota.id).exists() :
            
            vacuna = Vacuna_tipoB.objects.get(mascota_id = mascota.id)           
            if edad_meses > 4 :
                return [fecha_ingresada > vacuna.fecha_aplicacion + relativedelta(years=1),"No se puede aplicar la vacuna por que no a pasado el año de espera"] 
        else: 
            if edad_meses < 4:
                return [False,"La mascota no tiene todavia mas de 4 meses de edad , para aplicarle la vacuna tipo B"]
            else:
               return[True,""] 
    
    if (tipo != "A" and tipo != "B"):
        return [True,""]


def descuento(monto,descuento):
    return float(monto) - float(descuento)