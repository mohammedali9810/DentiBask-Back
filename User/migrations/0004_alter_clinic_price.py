# Generated by Django 4.2.3 on 2023-11-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_alter_clinic_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]