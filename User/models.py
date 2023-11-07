import datetime

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


############---------Payment-Info MODEL---------############
class Pay_inf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    exp_date = models.DateField()

############---------User/Vendor-Info MODEL---------############
class Add_info(models.Model):
    # vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True)
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

################################################################################################################################

############---------Order MODEL---------############
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

############---------OrderItem MODEL---------############
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('order_id', 'product_id')

############---------Clinic MODEL---------############
class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    desc = models.TextField(blank=True)
    location = models.CharField(max_length=50)
    area = models.FloatField()
    price = models.DecimalField(decimal_places=2, max_digits=2,default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

############---------Rent MODEL---------############
class Rent(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_months = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=2)
    renter = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Calculate duration in months based on start_date and end_date
        if self.start_date and self.end_date:
            self.duration_months = (
                    (self.end_date.year - self.start_date.year) * 12
                    + (self.end_date.month - self.start_date.month)
            )
        super(Rent, self).save(*args, **kwargs)



## Not Needed !!!
# ############---------Vendor MODEL---------############
# class Vendor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#     phone = models.CharField(max_length=11,
#         validators=[
#             RegexValidator(
#                 regex="^01[0|1|2|5][0-9]{8}$",
#                 message="Phone must start with 010, 011, 012, or 015 and contain 11 digits",
#                 code="invalid number",
#             )
#         ], blank=True)
#     def __str__(self):
#         return self.name

## not needed !!!