# Generated by Django 4.2 on 2023-06-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_visitas_cant_desparacitante_visitas_codigo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campana',
            name='fecha_fin',
            field=models.DateField(error_messages={'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD'}),
        ),
    ]