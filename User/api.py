from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view
from .models import Customer, Pay_inf, Add_info, Order, OrderItem, Clinic, Rent ,Transaction
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSerializer,
                          OrderItemSeriallizer, RentSeriallizer, AddInfoSeriallizer, PayInfoSeriallizer,TransactionSeriallizer)
from Products.api import CustomPagination
from django.contrib.auth.models import User
from .token import account_activation_token
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token
from rest_framework.exceptions import ValidationError


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
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


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


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSeriallizer
    lookup_field = 'pk'


class PayInfoViewSet(viewsets.ModelViewSet):
    queryset = Pay_inf.objects.all()
    serializer_class = PayInfoSeriallizer
    lookup_field = 'pk'


class AddInfoViewSet(viewsets.ModelViewSet):
    queryset = Add_info.objects.all()
    serializer_class = AddInfoSeriallizer
    lookup_field = 'pk'


class MyObtainToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
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
    print(email)
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

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        customer = serializer.save()

        # Send activation email
        # current_site = get_current_site(request)
        custom_activation_url = "localhost:3000/activate"
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('acc_active_email.html', {
            'user': customer,
            'domain': custom_activation_url,
            'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
            'token': account_activation_token.make_token(customer),
        })
        to_email = serializer.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        # Provide a success response with a redirect URL and message
        # redirect_url = reverse('login')  # Adjust this based on your URL configuration
        redirect_url = reverse('activate', args=[urlsafe_base64_encode(force_bytes(customer.pk)),account_activation_token.make_token(customer)])
        success_message = 'Check your email to activate your account.'
        return Response({
             'redirect_url': redirect_url,
            'success_message': success_message,
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                          location=location, area=area, price=price, image=image)
    return Response({"msg": "Clinic added."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_clinic(request):
    customer_id = request.auth.payload.get("user_id")
    clinics = Clinic.objects.filter(user=customer_id)
    serializer = ClinicSeriallizer(clinics, many=True)
    serialized_clinics = serializer.data
    return Response({"clinics": serialized_clinics}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_clinics(request):
    paginator = CustomPagination()
    clinics = Clinic.objects.all()
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
        clinic.delete()
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
        customer.delete()
        user.delete()
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer(request):
    customer_id = request.auth.payload.get('user_id')
    customer = Customer.objects.get(pk=customer_id)
    user = User.objects.get(pk=customer_id)
    password = request.data.get('vertifypassword')

    if user.check_password(password):
        try:
            phone = request.data.get('phone')
            image = request.data.get('image')
            username = request.data.get('username')
            new_password = request.data.get('password')

            if phone:
                customer.phone = phone
            if image:
                customer.image = image
            if username:
                user.username = username
                user.email = username
                customer.name = username
            if new_password:
                user.set_password(new_password)

            customer.save()
            user.save()

            return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": "Error updating data", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Wrong data"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_order(request):
   customer_id = request.auth.payload.get("user_id")
   orders = Order.objects.filter(user=customer_id)
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
   transactions = Transaction.objects.filter(user=customer_id)
   serializer = TransactionSeriallizer(transactions, many=True)
   serialized_transactions = serializer.data
   return Response({"transactions": serialized_transactions}, status=status.HTTP_200_OK)