# Generated by Django 4.2 on 2023-06-11 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Campania', '0002_remove_donaciones_cliente_donaciones_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donaciones',
            old_name='campana',
            new_name='campania',
        ),
    ]
