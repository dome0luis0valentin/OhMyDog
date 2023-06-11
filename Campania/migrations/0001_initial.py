# Generated by Django 4.2 on 2023-06-10 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0026_merge_0023_mascota_perdida_0025_alter_user_descuento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('campana', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.campana')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.cliente')),
            ],
        ),
    ]
