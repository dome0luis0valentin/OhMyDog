# Generated by Django 4.1.5 on 2023-07-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_prestador_servicios_vivo_alter_campana_fecha_fin'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador_servicios',
            name='deshabilitado_hasta',
            field=models.DateField(default='2023-07-04', error_messages={'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD'}),
        ),
    ]
