# Generated by Django 4.1.5 on 2023-06-24 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariotinder',
            name='sexo',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]