# Generated by Django 4.1.5 on 2023-05-04 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_cliente_nombre_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nombre_usuario',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='password',
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]