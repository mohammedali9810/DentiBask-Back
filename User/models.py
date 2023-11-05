from django.db import models
from Products.models import Product
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

############---------Customer MODEL---------############
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=11,
        validators=[
            RegexValidator(
                regex="^01[0|1|2|5][0-9]{8}$",
                message="Phone must start with 010, 011, 012, or 015 and contain 11 digits",
                code="invalid number",
            )
        ], blank=True)

    def __str__(self):
        return self.name


############---------Vendor MODEL---------############
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=11,
        validators=[
            RegexValidator(
                regex="^01[0|1|2|5][0-9]{8}$",
                message="Phone must start with 010, 011, 012, or 015 and contain 11 digits",
                code="invalid number",
            )
        ], blank=True)

    def __str__(self):
        return self.name

############---------Payment-Info MODEL---------############

class Pay_inf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    exp_date = models.DateField()

############---------User/Vendor-Info MODEL---------############
class Add_info(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    birth = models.DateField()
    address = models.TextField()
    pay_inf = models.ForeignKey(Pay_inf, on_delete=models.CASCADE)
    country = models.CharField(max_length=40, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics", blank=True)

    def __str__(self):
        if self.vendor:
            return f"Vendor: {self.vendor.name}"
        elif self.customer:
            return f"Customer: {self.customer.name}"
        else:
            return "No associated user"

############---------ِOrder MODEL---------############
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_date = models.DateField()

    def __str__(self):
        return f"Order for {self.user.username}"

############---------Cart MODEL---------############
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

############---------Cart-Items MODEL---------############
class Cart_Items(models.Model):
    id = models.AutoField(primary_key=True)
    cart_id = models.OneToOneField(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product)
    quantity = models.IntegerField()