# Generated by Django 4.0 on 2023-05-08 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={'verbose_name_plural': 'users'},
        ),
    ]