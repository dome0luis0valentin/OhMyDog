# Generated by Django 4.1.5 on 2023-05-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_mascota_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='foto',
            field=models.ImageField(blank=True, error_messages={'invalid': 'El archivo debe ser una imagen'}, upload_to='imagenes/'),
        ),
    ]
