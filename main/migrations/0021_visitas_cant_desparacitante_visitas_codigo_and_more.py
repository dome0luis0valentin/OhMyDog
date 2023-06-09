# Generated by Django 4.1.5 on 2023-06-02 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_user_id_visitas_cliente_alter_visitas_peso'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitas',
            name='cant_desparacitante',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='codigo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='visitas',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.cliente'),
        ),
    ]
