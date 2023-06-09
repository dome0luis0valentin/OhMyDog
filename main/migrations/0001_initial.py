# Generated by Django 4.1.5 on 2023-05-12 21:29

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_veterinario', models.BooleanField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campana',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('motivo', models.CharField(max_length=50)),
                ('fecha_fin', models.DateTimeField()),
                ('Total_donado', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('veterinario', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Intentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField(default=0)),
                ('estado', models.CharField(choices=[('b', 'bloqueado'), ('n', 'no bloqueado')], default='n', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.IntegerField()),
                ('direccion', models.CharField(max_length=200)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Prestador_Servicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('p', 'Paseador'), ('c', 'Cuidador')], default='p', help_text='Tipo de servicio que presta la persona', max_length=1)),
                ('datos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('asistio', models.BooleanField()),
                ('banda_horaria', models.CharField(choices=[('M', 'Mañana'), ('T', 'Tarde')], default='M', help_text='Horario en el que puede ir a la veterinaria mañana(7 AM - 12 PM) o tarde (12 PM a 6 PM', max_length=1)),
                ('motivo', models.CharField(choices=[('C', 'Consulta'), ('U', 'Urgencia'), ('S', 'Castración'), ('A', 'Vacunación de tipo A'), ('B', 'Vacunación de tipo B'), ('D', 'Desparasitación')], default='C', max_length=1)),
                ('estado', models.CharField(blank=True, choices=[('E', 'Esperando Confirmacion'), ('A', 'Aceptado'), ('R', 'Rechazado')], default='E', max_length=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Red_Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('usuario', models.CharField(max_length=70)),
                ('dueno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.prestador_servicios')),
            ],
        ),
        migrations.CreateModel(
            name='Mascota_Adopcion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('raza', models.CharField(max_length=1000)),
                ('fecha_nac', models.DateField()),
                ('estado', models.CharField(blank=True, choices=[('a', 'Adoptado'), ('e', 'Esperando')], default='e', help_text='Estado del perro', max_length=1)),
                ('dueno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('raza', models.CharField(max_length=1000)),
                ('fecha_nac', models.DateField()),
                ('foto', models.FileField(blank=True, upload_to='imaganes/')),
                ('dueno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='datos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.persona'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='mascotas',
            field=models.ManyToManyField(blank=True, to='main.mascota'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='mascotas_adopcion',
            field=models.ManyToManyField(blank=True, to='main.mascota_adopcion'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
