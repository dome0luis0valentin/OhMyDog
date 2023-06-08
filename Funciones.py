import re,string,random
from django.core.mail import EmailMessage
from datetime import datetime
from main.models import User


def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(10))
    return contrasena


def enviar_nueva_contraseña(user, asunto):
    remitente = 'grupo21ing2@gmail.com'  # Dirección de correo electrónico del remitente
    nueva_contraseña = generar_contrasena()
    mensaje = "Esta es tu nueva contraseña: "+nueva_contraseña  # Contenido del mensaje

    email = EmailMessage(asunto, mensaje, to=[user])
    email.send()

    return nueva_contraseña

def cadena_is_valid(cadena):
    if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$", cadena):
        return False
    return True

def numero_is_valid(numero):
    try:
        num = int(numero)
        return num>0
    except:
        return False

def todos_numeros(*cadenas):
    for cadena in cadenas:
        try:
            numero = int(cadena)
            if numero <= 0:
                return False
        except ValueError:
            return False
    return True


def todos_cadenas(*cadenas):
    for cadena in cadenas:
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$", cadena):
            return False
    return True

def dni_is_valid(dni):
    try:
        dni = int(dni)
        return True
    except:
        return False
    
def fecha_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada >= hoy
    except:
        return False
    
def fecha_anterior_is_valid(fecha):
    try:
        hoy = datetime.now().date()
        fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_ingresada <= hoy
    except:
        # El usuario no existe en la base de datos
        return False
    

def usuario_is_valid(username):
    try:
        user = User.objects.get(email=username)
        # El usuario existe en la base de datos
        return True
    except User.DoesNotExist:
        # El usuario no existe en la base de datos
        return False
    
   
   
# evalua si el dato ingresado en un numero real 
def es_numero_real_positivo(dato):
    try:
        numero = float(dato)
        if numero > 0:
            return True
        else:
            return False
    except ValueError:
        return False

