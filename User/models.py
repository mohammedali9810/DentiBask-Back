from django.db import models
from Products.models import Product
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

############---------Customer MODEL---------############
class Customer(models.Model):
    id = models.AutoField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    # about = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=11,
        validators=[
            RegexValidator(
                regex="^01[0|1|2|5][0-9]{8}$",
                message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
                code="invalid number",
            )
        ], blank=True)

    def __str__(self):
        return f"{self.user.username}"


############---------Vendor MODEL---------############
class Vendor(models.Model):
    id = models.AutoField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=200)
    #about = models.TextField()
    email = models.EmailField()
    phone = models.IntegerField(max_length=11,
        validators=[
            RegexValidator(
                regex="^01[0|1|2|5][0-9]{8}$",
                message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
                code="invalid number",
            )
        ], blank=True)


    def __str__(self):
        return self.name

############---------Payment-Info MODEL---------############

class Pay_inf(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    exp_dat = models.DateField()

############---------User/Vendor-Info MODEL---------############
class Add_info(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    birth = models.DateField()
    address = models.TextField()
    pay_inf = models.ForeignKey(Pay_inf)
    country = models.CharField(max_length=40, blank=True)
    image = models.ImageField(
         default="default.jpg", upload_to="profile_pics", blank=True
    )
    def __str__(self):
        return self.name

############---------ِOrder MODEL---------############
class Order (models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    order_date = models.DateField()
