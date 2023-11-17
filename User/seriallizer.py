from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from Products.models import Product
from .models import Customer, Pay_inf, Add_info, Order, OrderItem, Clinic, Rent, Transaction


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

class OrderItemSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    def create(self, validated_data):
        product_price = validated_data.get('product_id').price
        total = product_price * validated_data['quantity']
        orderitem_data = {
            'order_id': validated_data['order_id'],
            'product_id': validated_data['product_id'],
            'quantity': validated_data['quantity'],
            'price': product_price,
            'total': total,
        }
        orderitem = OrderItem.objects.create(**orderitem_data)
        return orderitem

class OrderSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ClinicSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
class RentSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'

    def validate(self, data):
        # Ensure that the start date is before the end date
        if data.get('start_date') and data.get('end_date') and data['start_date'] >= data['end_date']:
            raise serializers.ValidationError({'end_date': _('End date must be after the start date.')})

        # Calculate duration in months based on start_date and end_date
        if data.get('start_date') and data.get('end_date'):
            months = ((data['end_date'].year - data['start_date'].year) * 12
                    + (data['end_date'].month - data['start_date'].month))
            if months > 0:
                data['duration_months'] = months
            else:
                raise serializers.ValidationError({'duration': _(' Renting Duration is at least 1 month.')})

        # Ensure that the price is not a negative value
        if data.get('price', 0) < 0:
            raise serializers.ValidationError({'price': _('Price must not be a negative value.')})

        return data


class TransactionSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['is_deleted']

    def create(self, validated_data):
        order = validated_data['order_id']
        order_amount = order.total  # Use the total field directly
        transaction_data = {
            'order_id': order,
            'amount': order_amount,
            'user': validated_data['user'],
        }
        transaction = Transaction.objects.create(**transaction_data)
        return transaction



class CustomerSerializer(serializers.ModelSerializer):
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
            'image':'',
        }

        # Extract user data
        user_data = {
            'username': validated_data['email'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'is_active': False
        }

        # Create User and Customer
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **customer_data)

        return customer

