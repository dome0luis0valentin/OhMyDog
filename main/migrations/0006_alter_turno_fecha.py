# Generated by Django 4.1.5 on 2023-05-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_cliente_veterinario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='fecha',
            field=models.DateField(error_messages={'invalid': 'Fecha incorrecta. Use el formato AAAA-MM-DD'}),
        ),
    ]
