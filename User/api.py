from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view
from .models import Customer,Pay_inf,Add_info,Order,OrderItem,Clinic,Rent
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSeriallizer,
                          OrderItemSeriallizer, RentSeriallizer, AddInfoSeriallizer,PayInfoSeriallizer)
from .token import account_activation_token
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from .seriallizer import CustomerSerializer
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
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

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})