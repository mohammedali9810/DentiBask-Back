from rest_framework import serializers
from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
class CustomerSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PayInfoSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Pay_inf
        fields = '__all__'
class AddInfoSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Add_info
        fields = '__all__'

class OrderSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class OrderItemSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
class ClinicSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
class RentSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'