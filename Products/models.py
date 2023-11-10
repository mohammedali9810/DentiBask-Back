from django.db import models
import os
from django.utils import timezone


def unique_image_name(instance, filename):
    base, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'images/category/{base}_{timestamp}{extension}'
# Create your models here.
############---------Category MODEL---------############
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(null=False, blank=False,upload_to=unique_image_name)

    #Admin_id
    def __str__(self):
        return self.name

def unique_image_product(instance, filename):
    base, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'images/product/{base}_{timestamp}{extension}'
############---------PRODUCT MODEL---------############
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)
    image = models.ImageField(null=False, blank=False,upload_to=unique_image_product)
    stock = models.IntegerField(default=0)
    Categ_id = models.ForeignKey(Category, on_delete=models.CASCADE)


    def get_img(self):
        return f"/media/{self.image}"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.price = round(float(self.price), 2)
        super(Product, self).save(*args, **kwargs)
