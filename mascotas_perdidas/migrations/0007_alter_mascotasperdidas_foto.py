# Generated by Django 4.1.5 on 2023-06-03 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas_perdidas', '0006_alter_mascotasperdidas_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascotasperdidas',
            name='foto',
            field=models.ImageField(blank=True, upload_to='mascotas_perdidas/'),
        ),
    ]
