# Generated by Django 4.2.3 on 2023-11-17 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_alter_customer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rent',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]