# Generated by Django 4.0 on 2023-05-13 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_decisiontreemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisiontreemodel',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]