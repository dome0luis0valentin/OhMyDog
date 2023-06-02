# Generated by Django 4.1.5 on 2023-06-02 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_visitas'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitas',
            name='fecha',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='mascota',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.mascota'),
        ),
        migrations.AddField(
            model_name='visitas',
            name='motivo',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='observaciones',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='peso',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
