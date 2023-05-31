# Generated by Django 4.1.5 on 2023-05-20 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_vacuna_tipob'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador_servicios',
            name='zona',
            field=models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(25)]),
        ),
    ]