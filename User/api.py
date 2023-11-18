from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view

from Products.models import Product
from .models import Customer, Pay_inf, Add_info, Order, OrderItem, Clinic, Rent, Transaction
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSerializer,
                          OrderItemSeriallizer, RentSeriallizer, AddInfoSeriallizer, PayInfoSeriallizer, TransactionSeriallizer)
from Products.api import CustomPagination
from django.contrib.auth.models import User
from .token import account_activation_token
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token
from rest_framework.exceptions import ValidationError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class PayInfoViewSet(viewsets.ModelViewSet):
    queryset = Pay_inf.objects.all()
    serializer_class = PayInfoSeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class AddInfoViewSet(viewsets.ModelViewSet):
    queryset = Add_info.objects.all()
    serializer_class = AddInfoSeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
class MyObtainToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        print(password)
        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            token = super().post(request, *args, **kwargs).data
            return Response({"token": token})
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def check_email(request):
    email = request.GET.get('username')
    try:
        customer = Customer.objects.get(email=email)
    except:
        return Response({"msg": "email Not found."}, status=status.HTTP_400_BAD_REQUEST)
    if customer:
        print(customer)
        return Response({"msg": "email found."}, status=status.HTTP_200_OK)
    return Response({"msg": "email Not found."}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = CustomerSerializer(data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()
            print("Passed Serializer!")

            # Set up your email content
            custom_activation_url = "localhost:3000/activate"
            mail_subject = 'Please Activate Your Account!'
            message = render_to_string('acc_active_email.html', {
                'user': customer,
                'domain': custom_activation_url,
                'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                'token': account_activation_token.make_token(customer),
            })
            to_email = serializer.validated_data.get('email')
            print("Passed Email Construct")

            # Establish an SMTP connection and send the email
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login('djang7207@gmail.com', 'nhdk jhrd pqtk bonb')

                    msg = MIMEMultipart()
                    msg.attach(MIMEText(message, "html"))
                    msg["Subject"] = mail_subject
                    msg["From"] = 'djang7207@gmail.com'
                    msg["To"] = to_email

                    server.sendmail('djang7207@gmail.com', to_email, msg.as_string())

                print("Email sent successfully.")
            except Exception as e:
                print(f"Error sending email: {e}")

            # Provide a success response with a redirect URL and message
            redirect_url = reverse('activate', args=[urlsafe_base64_encode(force_bytes(customer.pk)),
                                                     account_activation_token.make_token(customer)])
            success_message = 'Check your email to activate your account.'
            return Response({
                'redirect_url': redirect_url,
                'success_message': success_message,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)



def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Activation successful'})
    else:
        return JsonResponse({'error': 'Invalid activation link'}, status=400)


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def get_all_customers(request):
    paginator = CustomPagination()
    customers = Customer.objects.filter(is_active=False)
    paginated_customers = paginator.paginate_queryset(customers, request)
    seriallized_customers = CustomerSerializer(paginated_customers,many=True).data
    return paginator.get_paginated_response(seriallized_customers)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_clinic(request):
    title = request.data.get('title')
    location = request.data.get('location')
    area = request.data.get('area')
    price = request.data.get('price')
    image = request.data.get('image')
    desc = request.data.get('desc')
    customer_id = request.auth.payload.get("user_id")
    customer = Customer.objects.get(pk=customer_id)
    # Validate required fields
    if not all([title, location, area, price, image]):
        raise ValidationError(
            {"msg": "Missing required fields."}, code=status.HTTP_400_BAD_REQUEST)
    # Validate numeric fields
    try:
        area = float(area)
        price = float(price)
    except ValueError:
        raise ValidationError(
            {"msg": "Invalid numeric values for area or price."}, code=status.HTTP_400_BAD_REQUEST)
    Clinic.objects.create(title=title, desc=desc, user=customer,
                          location=location, area=area, price=price, image=image, is_deleted=False)
    return Response({"msg": "Clinic added."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_clinic(request):
    customer_id = request.auth.payload.get("user_id")
    clinics = Clinic.objects.filter(user=customer_id,is_deleted=False)
    serializer = ClinicSeriallizer(clinics, many=True)
    serialized_clinics = serializer.data
    return Response({"clinics": serialized_clinics}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_clinics(request):
    paginator = CustomPagination()
    clinics = Clinic.objects.filter(is_deleted=False)
    paginated_clinics = paginator.paginate_queryset(clinics, request)

    # Serialize the paginated products
    serializer = ClinicSeriallizer(paginated_clinics, many=True)
    serialized_clinicis = serializer.data

    # Return the paginated response
    return paginator.get_paginated_response(serialized_clinicis)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_clinic(request):
    customer_id = request.auth.payload.get('user_id')
    customer = Customer.objects.get(pk=customer_id)
    clinic_id = request.data.get('clinic_id')
    try:
        clinic = Clinic.objects.get(pk=clinic_id)
    except Clinic.DoesNotExist:
        return Response({"msg": "Clinic not found."}, status=status.HTTP_404_NOT_FOUND)

    if customer == clinic.user:
        clinic.is_deleted = True
        clinic.save()
        return Response({"msg": "Clinic deleted."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"msg": "Not authorized to delete this clinic."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request):
    try:
        customer_email = request.data.get('customer_email')
        customer = Customer.objects.get(email=customer_email)
        user = User.objects.get(email=customer_email)
        customer.is_active = False
        customer.save()
        user.is_active = False
        user.save()
    except:
        return Response({"msg": "Can not find user or customer."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"msg": "User Found."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userdata(request):
    customer_id = request.auth.payload.get('user_id')
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return Response({"msg": "Can not find user or customer."}, status=status.HTTP_400_BAD_REQUEST)
    serialized_customer = CustomerSerializer(customer).data
    return Response(serialized_customer, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_customer(request):
    try:
        customer_id = request.auth.payload.get('user_id')
        customer = Customer.objects.get(pk=customer_id)
        user = User.objects.get(pk=customer_id)
        password = request.data.get('vertifypassword')

        if user.check_password(password):
            new_phone = request.data.get('phone', '')
            if new_phone:
                customer.phone = new_phone
            new_username = request.data.get('username', '')
            if new_username:
                customer.name = new_username
            new_password = request.data.get('password')
            if new_password:
                user.set_password(new_password)
            user.full_clean()
            user.save()

            if 'image' in request.data and request.data['image']:
                customer.image = request.data['image']
                customer.full_clean()
                customer.save()
                return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
            else:
                customer.full_clean()
                customer.save()
                return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"msg": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({"msg": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_order(request):
    customer_id = request.auth.payload.get("user_id")
    orders = Order.objects.filter(user=customer_id,is_deleted=False)
    serializer = OrderSeriallizer(orders, many=True)
    serialized_orders = serializer.data
    return Response({"orders": serialized_orders}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rent(request):
    customer_id = request.auth.payload.get("user_id")
    rents = Rent.objects.filter(renter=customer_id)
    serializer = RentSeriallizer(rents, many=True)
    serialized_rents = serializer.data
    return Response({"rents": serialized_rents}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transaction(request):
    customer_id = request.auth.payload.get("user_id")
    transactions = Transaction.objects.filter(user=customer_id,is_deleted=False)
    serializer = TransactionSeriallizer(transactions, many=True)
    serialized_transactions = serializer.data
    return Response({"transactions": serialized_transactions}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_orders(request):
    paginator = CustomPagination()
    orders = Order.objects.filter(is_deleted=False)
    paginated_orders = paginator.paginate_queryset(orders, request)

    serializer = OrderSeriallizer(paginated_orders, many=True)
    serialized_orders = serializer.data

    return Response({"orders": serialized_orders}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_rents(request):
    paginator = CustomPagination()
    rents = Rent.objects.filter(is_deleted=False)
    paginated_rents = paginator.paginate_queryset(rents, request)

    serializer = RentSeriallizer(paginated_rents, many=True)
    serialized_rents = serializer.data

    return Response({"rents": serialized_rents}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_transactions(request):
    paginator = CustomPagination()
    transactions = Transaction.objects.filter(is_deleted=False)
    paginated_transactions = paginator.paginate_queryset(transactions, request)

    serializer = TransactionSeriallizer(paginated_transactions, many=True)
    serialized_transactions = serializer.data

    return Response({"transactions": serialized_transactions}, status=status.HTTP_200_OK)


def get_items_in_order(order_id):
    items = OrderItem.objects.filter(order_id=order_id)
    return items

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def get_one_user_orders(request):
    customer_email = request.GET.get('customer_email')
    customer = Customer.objects.get(email=customer_email)
    orders = Order.objects.filter(user=customer.user.id,is_deleted=False)
    serializer = OrderSeriallizer(orders, many=True)
    serialized_orders = serializer.data
    return Response({"orders": serialized_orders}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        customer_email = request.auth.payload.get('user_id')
        try:
            user_instance = Customer.objects.get(pk=customer_email)
        except Customer.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        orderitems_data = request.data.get('orderitem_set', [])
        if not orderitems_data:
            return Response({"msg":"Items must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        total = 0

        # Create an Order instance
        order_serializer = OrderSeriallizer(data={'user': user_instance, 'status': 'Processing', 'total': 0,'is_deleted': False})
        if order_serializer.is_valid():
            order = order_serializer.save()
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for orderitem_data in orderitems_data:
            # Add the order_id to the orderitem_data
            orderitem_data['order_id'] = order.id
            orderitem_serializer = OrderItemSeriallizer(data=orderitem_data)
            if orderitem_serializer.is_valid():
                order_item = orderitem_serializer.save()
            else:
                order.delete()
                return Response(orderitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Update total for the Order
            total += order_item.total

        # Update the total field for the Order
        order.total = total
        order.save()

        return Response({"order_id": "Order created successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def get_order_items_admin(request):
    order_id = request.GET.get('order_id')
    print(order_id)
    try:
        orderitems = OrderItem.objects.filter(order_id=order_id)
        print(orderitems)
    except OrderItem.DoesNotExist:
        return Response({"msg":"can not find order items for this order"}, status=status.HTTP_400_BAD_REQUEST)
    seriallized_items = OrderItemSeriallizer(orderitems,many=True).data
    return Response(seriallized_items,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request):
    customer_id = request.auth.payload.get("user_id")
    customer = Customer.objects.get(pk=customer_id)
    order_id = request.data.get("order_id")
    order = Order.objects.get(pk=order_id)

    if customer_id == order.user.user.id:
        order.status = "Processing"
        order.save()

        # Use the serializer to create a Transaction instance
        serializer = TransactionSeriallizer(data={'order_id': order_id, 'user': customer})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Transaction has been done successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    customer_id = request.auth.payload.get("user_id")
    order_id = request.data.get("order_id")
    order = Order.objects.get(pk=order_id)
    print(order_id)
    if customer_id == order.user.user.id:
        order.status = "Cancelled"
        order.save()
        return Response({"msg":"Order has been Cancelled"},status=status.HTTP_200_OK)
    else:
        return Response({"msg": "You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)