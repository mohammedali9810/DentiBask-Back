from django.db import models
import os
from django.utils import timezone
# views.py

def unique_image_name(instance, filename):
    if instance.image and filename:
        base, extension = os.path.splitext(filename)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'images/category/{base}_{timestamp}{extension}'
    else:
        return instance.image.name

############---------Category MODEL---------############
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    desc = models.TextField()
    image = models.ImageField(null=False, blank=False,upload_to=unique_image_name)
    is_deleted = models.BooleanField(default=False)
    #Admin_id

def unique_image_product(instance, filename):
    if instance.image and filename:
        base, extension = os.path.splitext(filename)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'images/product/{base}_{timestamp}{extension}'
    else:
        return instance.image.name

############---------PRODUCT MODEL---------############
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)
    image = models.ImageField(null=False, blank=False,upload_to=unique_image_product)
    stock = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    Categ_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_img(self):
        return f"/media/{self.image}"


    def save(self, *args, **kwargs):
        self.price = round(float(self.price), 2)
        super(Product, self).save(*args, **kwargs)
