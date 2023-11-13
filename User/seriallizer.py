from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
class CustomerSeriallizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'password']

    def create(self, validated_data):
        # Extract customer data
        customer_data = {
            'name': validated_data['name'],
            'email': validated_data['email'],
            'phone': validated_data['phone']
        }

        # Extract user data
        user_data = {
            'username': validated_data['email'],
            'email': validated_data['email'],
            'password': validated_data['password'],
        }

        # Create User and Customer
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **customer_data)

        return customer



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

