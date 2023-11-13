from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view
from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSeriallizer,
                          OrderItemSeriallizer, RentSeriallizer, AddInfoSeriallizer,PayInfoSeriallizer)
from Products.api import CustomPagination
from django.contrib.auth.models import User
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
    serializer_class = CustomerSeriallizer
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
from rest_framework.exceptions import ValidationError

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
        raise ValidationError({"msg": "Missing required fields."}, code=status.HTTP_400_BAD_REQUEST)
    # Validate numeric fields
    try:
        area = float(area)
        price = float(price)
    except ValueError:
        raise ValidationError({"msg": "Invalid numeric values for area or price."}, code=status.HTTP_400_BAD_REQUEST)
    Clinic.objects.create(title=title, desc=desc, user=customer, location=location, area=area, price=price, image=image)
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
@permission_classes([IsAuthenticated,IsAdminUser])
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