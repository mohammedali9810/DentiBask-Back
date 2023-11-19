# Generated by Django 4.2.3 on 2023-11-15 17:51

import User.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default=1, upload_to=User.models.unique_image_customer),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.customer'),
        ),
        migrations.AlterField(
            model_name='pay_inf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customer'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='renter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customer'),
        ),
    ]