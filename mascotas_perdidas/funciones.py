from Mensaje import *

def agregar_errores(form, fecha, perdida):
    if not fecha:
        form.errors['fecha'] = [MENSAJE_FECHA_POSTERIOR]

    if perdida:
        form.errors['mascota'] = [MENSAJE_MASCOTA_YA_PERDIDA]
        form.errors['nombre'] = [MENSAJE_MASCOTA_YA_PERDIDA]
        
    if form.errors:
        for field_name, errors in form.errors.items():
            if (field_name == 'foto'):
                form.errors['foto'] = [MENSAJE_IMAGEN_INVALIDA]