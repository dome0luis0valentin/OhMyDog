# Generated by Django 4.1.5 on 2023-06-03 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas_perdidas', '0005_mascotasperdidas_nombre_mascotasperdidas_raza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascotasperdidas',
            name='foto',
            field=models.FileField(blank=True, upload_to='mascotas_perdidas/'),
        ),
    ]