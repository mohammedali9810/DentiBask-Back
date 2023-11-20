# Generated by Django 4.2.3 on 2023-11-13 12:17

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='image',
            field=models.ImageField(default=1, upload_to=User.models.unique_image_clinic),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]