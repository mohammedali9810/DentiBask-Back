# Generated by Django 4.2.3 on 2023-11-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_clinic_desc_clinic_title_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay_inf',
            name='card_num',
            field=models.IntegerField(),
        ),
    ]