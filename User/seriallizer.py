from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
class CustomerSeriallizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'password','image']

    def create(self, validated_data):
        # Extract customer data
        customer_data = {
            'name': validated_data['name'],
            'email': validated_data['email'],
            'phone': validated_data['phone'],
            'image': validated_data['image']
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

    @action(detail=False, methods=['DELETE'])
    def delete_by_email(self, request):
        email = request.data.get('email')
        if email:
            try:
                customer = Customer.objects.get(email=email)
                customer.delete()
                return Response({"msg": "Customer deleted."}, status=status.HTTP_204_NO_CONTENT)
            except Customer.DoesNotExist:
                return Response({"msg": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"msg": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


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



class CustomerSerializer(serializers.ModelSerializer):
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
            'password': validated_data['password']
        }

        # Create User and Customer
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **customer_data)

        return customer

