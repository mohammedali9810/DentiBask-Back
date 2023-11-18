from django.utils import timezone
import os

from django.db import models
from Products.models import Product
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

def unique_image_customer(instance, filename):
    if instance.image and filename:
        base, extension = os.path.splitext(filename)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'images/customer/{base}_{timestamp}{extension}'
    else:
        return instance.image.name
############ ---------Customer MODEL---------############


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11,
                             validators=[
                                 RegexValidator(
                                     regex="^01[0|1|2|5][0-9]{8}$",
                                     message="Phone must start with 010, 011, 012, or 015 and contain 11 digits",
                                     code="invalid number",
                                 )
                             ], blank=True)
    image = models.ImageField(upload_to=unique_image_customer, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    def _str_(self):
        return self.email


############ ---------Payment-Info MODEL---------############
class Pay_inf(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    exp_date = models.DateField()
    card_num = models.IntegerField()

############ ---------User/Vendor-Info MODEL---------############


class Add_info(models.Model):
    # vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    birth = models.DateField()
    address = models.TextField()
    pay_inf = models.ForeignKey(Pay_inf, on_delete=models.CASCADE)
    country = models.CharField(max_length=40, blank=True)

    def _str_(self):
        if self.customer:
            return f"Customer: {self.customer.name}"
        else:
            return "No associated user"

################################################################################################################################

############ ---------Order MODEL---------############


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # address = models.CharField(max_length=50)
    STATUS_CHOICES = [
        ('Cancelled', 'Cancelled'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Processing')
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

############ ---------OrderItem MODEL---------############


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=8,editable=False)
    quantity = models.IntegerField()
    total = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('order_id', 'product_id')


def unique_image_clinic(instance, filename):
    base, extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'images/clinic/{base}_{timestamp}{extension}'
############ ---------Clinic MODEL---------############


class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    desc = models.TextField(blank=True)
    location = models.CharField(max_length=50)
    area = models.FloatField()
    price = models.FloatField(default=0)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_image_clinic)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
############ ---------Rent MODEL---------############


class Rent(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_months = models.IntegerField(editable=False)
    price = models.FloatField()
    renter = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Calculate duration in months based on start_date and end_date
        if self.start_date and self.end_date:
            self.duration_months = (
                (self.end_date.year - self.start_date.year) * 12
                + (self.end_date.month - self.start_date.month)
            )
        super(Rent, self).save(*args, **kwargs)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField(editable=False)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transaction')
    is_deleted = models.BooleanField(default=False)