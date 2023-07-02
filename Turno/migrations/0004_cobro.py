# Generated by Django 4.1.5 on 2023-06-30 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_alter_visitas_monto'),
        ('Turno', '0003_alter_veterinarias_de_turno_arch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('fecha', models.DateField()),
                ('motivo', models.CharField(max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.cliente')),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.mascota')),
            ],
        ),
    ]