# Generated by Django 4.0 on 2023-05-08 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_usermodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={},
        ),
        migrations.AlterModelTable(
            name='usermodel',
            table='users',
        ),
    ]