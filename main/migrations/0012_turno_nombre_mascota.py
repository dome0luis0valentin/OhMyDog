# Generated by Django 4.2 on 2023-05-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_rename_nombre_red_social_nombre_red_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='nombre_mascota',
            field=models.TextField(default='null'),
        ),
    ]
