from Mensaje import *

def agregar_errores(form, fecha):
    if not fecha:
        form.errors['fecha'] = [MENSAJE_FECHA_POSTERIOR]

    if form.errors:
        for field_name, errors in form.errors.items():
            if (field_name == 'foto'):
                form.errors['foto'] = [MENSAJE_IMAGEN_INVALIDA]