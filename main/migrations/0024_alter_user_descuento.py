# Generated by Django 4.2 on 2023-06-05 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_user_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
    ]
