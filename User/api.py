from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSeriallizer,
                          OrderItemSeriallizer, RentSeriallizer, AddInfoSeriallizer,PayInfoSeriallizer)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSeriallizer
    lookup_field = 'pk'

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSeriallizer
    lookup_field = 'pk'
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSeriallizer
    lookup_field = 'pk'
class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSeriallizer
    lookup_field = 'pk'
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
