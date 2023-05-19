# Generated by Django 4.2 on 2023-05-17 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_turno_nombre_mascota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='nombre_mascota',
        ),
        migrations.AddField(
            model_name='turno',
            name='mascota',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.mascota'),
        ),
    ]