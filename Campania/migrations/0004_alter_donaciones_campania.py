# Generated by Django 4.2 on 2023-06-11 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campania', '0003_rename_campana_donaciones_campania'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donaciones',
            name='campania',
            field=models.CharField(max_length=255),
        ),
    ]
