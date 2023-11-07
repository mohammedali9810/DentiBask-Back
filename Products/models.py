from django.db import models

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
    price = models.DecimalField(decimal_places=2, max_digits=2,default=0)
    image = models.ImageField(null=False, blank=False)
    stock = models.IntegerField(default=0)
    Categ_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    # vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    ## add stock


    def get_img(self):
        return f"/media/{self.image}"

    def __str__(self):
        return self.name