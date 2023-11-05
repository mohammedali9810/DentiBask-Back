from django.db import models
from User.models import Vendor
# Create your models here.
############---------Category MODEL---------############
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(null=False, blank=False)
    #Admin_id

    def __str__(self):
        return self.name

############---------PRODUCT MODEL---------############
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.FloatField()
    image = models.ImageField(null=False, blank=False)
    Categ_id = models.ForeignKey(Category) #, on_delete=models.CASCADE#
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def get_img(self):
        return f"/media/{self.image}"

    def __str__(self):
        return self.name