from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view
from django.shortcuts import get_object_or_404
from .models import Customer, Pay_inf, Add_info, Order, OrderItem, Clinic, Transaction
from Products.models import Product
from .seriallizer import (OrderSeriallizer, ClinicSeriallizer, CustomerSerializer, Cust_signin_ser,
                          OrderItemSeriallizer, AddInfoSeriallizer, PayInfoSeriallizer, TransactionSeriallizer, PasswordResetSerializer)
from Products.api import CustomPagination
from django.contrib.auth.models import User
from .token import account_activation_token, reset_token_signer, TokenGen
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from urllib.parse import quote
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ValidationError as djan_val_er
from django.core.signing import Signer
import uuid, ast, time
import json
################################
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
# from .token import verify_one_time_token
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import jwt
import requests
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


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


# class RentViewSet(viewsets.ModelViewSet):
#     queryset = Rent.objects.all()
#     serializer_class = RentSeriallizer
#     lookup_field = 'pk'
#     pagination_class = CustomPagination
#     permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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
# class MyObtainToken(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         if not username or not password:
#             return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if username == "oem":
#                 role = 'admin'
#             else:
#                 role = 'user'
#             token = super().post(request, *args, **kwargs).data
#             return Response({"token": token,"role": role})
#         else:
#             return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

class MyObtainToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        print(f"USER AUTHO LOGINO : {user}")
        # print(user.is_authenticated)

        if user is not None:
            if user.username == "oem":
                role = 'admin'
            else:
                role = 'user'

            token = super().post(request, *args, **kwargs).data
            return Response({"token": token, "role": role, "is_authenticated": True})
        else:
            return Response({"error": "Invalid username or password.", "is_authenticated": False}, status=status.HTTP_401_UNAUTHORIZED)




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

@api_view(['GET'])
def check_reg(request):
    email = request.GET.get('email')
    print(email)
    try:
        customer = Customer.objects.get(email=email)
        print(customer)
    except:
        return Response({"msg": "email Not found."}, status=status.HTTP_200_OK)
    if customer:
        print(customer)
        return Response({"msg": "email found."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"msg": "email Not found."}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = CustomerSerializer(data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Your existing Customer model, CustomerSerializer, and account_activation_token imports go here

# @receiver(pre_save, sender=Customer)
# def send_activation_email(sender, instance, **kwargs):
#     if not instance.pk:
#         custom_activation_url = "localhost:3000/activate"
#         mail_subject = 'Please Activate Your Account!'
#         message = render_to_string('acc_active_email.html', {
#             'user': instance,
#             'domain': custom_activation_url,
#             'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
#             'token': account_activation_token.make_token(instance),
#         })
#         to_email = instance.email
#
#         try:
#             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#                 server.login('djang7207@gmail.com', 'hfda kzdl rzhs nrjj')
#
#                 msg = MIMEMultipart()
#                 msg.attach(MIMEText(message, "html"))
#                 msg["Subject"] = mail_subject
#                 msg["From"] = 'djang7207@gmail.com'
#                 msg["To"] = to_email
#
#                 server.sendmail('djang7207@gmail.com', to_email, msg.as_string())
#
#             print("Email sent successfully.")
#         except Exception as e:
#             print(f"Error sending email: {e}")

# Your existing Customer model, CustomerSerializer, and account_activation_token imports go here
#################################################################################################
class MyOauthObtainToken(TokenObtainPairView):
    @classmethod
    def post(self, request, *args, **kwargs):
        role = 'user'
        token = super().post(request, *args, **kwargs).data
        return Response({"token": token, "role": role, "is_authenticated" :True})

@api_view(['POST'])
@permission_classes([AllowAny])
def google_signin(request):
    try:
        # Fetch Google's public keys from the JWK Set endpoint
        token = request.data.get('token')
        # jwks = requests.get(jwks_url).json()
        # token="211650131656-10hp9abqvemrbvo7v13o62hq48bs5ouk.apps.googleusercontent.com"
        # id_info = id_token.verify_oauth2_token(token, requests.Request(), jwks=jwks)
        # email = id_info['email']
        # name = id_info['name']
        # print(f"EMAILOO : {email}")
        # token = request.data.get('token')

        decoded_token = jwt.decode(token, algorithms=['HS256'], options={'verify_signature': False})
        print(f"Decoded token: {decoded_token}")
        email = decoded_token.get('email')
        name = decoded_token.get('name')
        picture = decoded_token.get('picture')
        print(f"DECODED EMAIL : {email}")
        print(f"DECODED NAME : {name}")
        print(f"DECODED PICTURE : {picture}")

        # verified_name = id_info['name']
        # verified_image = id_info['picture']


        # if verified_email != email:
        #     # Invalid email in the token
        #     return Response({"error": "Invalid social login credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the email already exists
        existing_customer = Customer.objects.filter(email=email).first()
        print(existing_customer)
        if existing_customer:
            token_data = generate_jwt_token(user)
            # Email exists, attempt login
            print("USER EXISTO")
            # user = authenticate(username=email, password='')  # No password needed for social login
            # print(f"USER AUTHO : {user}")
            # if user is not None:
            #     # Login successful
            #     if user.username == "oem":
            #         role = 'admin'
            #     else:
            #         role = 'user'
            #
            #     token = RefreshToken.for_user(user).access_token
            #     return Response({"token": token, "role": role, "is_authenticated": True})
            # else:
            #     # Invalid credentials
            #     return Response({"error": "Invalid social login credentials.", "is_authenticated": False}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Email does not exist, proceed with registration
            serializer = Cust_signin_ser(data={'email': email, 'name': name})
            if serializer.is_valid():
                customer = serializer.save()
                MyOauthObtainToken.post(request)
                # Generate token for the newly registered user
                # user = authenticate(username=email, password=None)
                # token = RefreshToken.for_user(user).access_token

                # You can include the activation email logic here if needed

                # Provide a success response with a redirect URL and message
                # redirect_url = reverse('activate', args=[urlsafe_base64_encode(force_bytes(customer.pk)),
                #                                          account_activation_token.make_token(customer)])
                # success_message = 'Check your email to activate your account.'
                # return Response({
                #     # 'redirect_url': redirect_url,
                #     'token': token,
                #     'role': 'user',  # You may customize the role as needed
                #     'is_authenticated': True,
                #     'success_message': success_message,
                # }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # except Exception as e:
    #     return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)
#################################################################################################
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()
            custom_activation_url = "localhost:3000/activate"
            mail_subject = 'Please Activate Your Account!'
            message = render_to_string('acc_active_email.html', {
                'user': customer,
                'domain': custom_activation_url,
                'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                'token': account_activation_token.make_token(customer),
            })
            to_email = serializer.validated_data.get('email')
            # Establish an SMTP connection and send the email
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    # server.starttls()
                    server.login('djang7207@gmail.com', 'hfda kzdl rzhs nrjj')

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
####################################################################################################
# Create a TimestampSigner instance
timestamp_signer = TimestampSigner()
# Instantiate TokenGenerator
account_activation_token2 = TokenGen()

@api_view(['POST'])
def reset_password_request(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        print(email)

        email = serializer.validated_data['email']
        print(f"Email: {email}")

        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.email}")

            # Generate a one-time-use reset token with expiration time
            reset_token = default_token_generator.make_token(user)

            # Include the token directly in the reset URL
            reset_url = f"http://localhost:3000/reset-password/confirm/{urlsafe_base64_encode(force_bytes(user.pk))}/{reset_token}/"

            print(f"Reset URL: {reset_url}")

        except User.DoesNotExist:
            return Response({'redirect_url': 'http://localhost:3000/Login', 'message': 'Email not found.'})
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Set up the email parameters
        sender_email = 'djang7207@gmail.com'
        subject = 'Password Reset'
        receiver_email = email

        # Create the MIME object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Create the message content
        customer = get_object_or_404(Customer, email=email)
        message_content = render_to_string('reset_password_email.html', {'user': customer.name, 'reset_url': reset_url})
        message.attach(MIMEText(message_content, 'html'))

        # Set the maximum number of retry attempts
        max_retries = 3
        # Set the delay between retry attempts in seconds
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(sender_email, 'hfda kzdl rzhs nrjj')
                    server.sendmail(sender_email, receiver_email, message.as_string())

                return Response(
                    {'redirect_url': 'http://localhost:3000/Login',
                     'message': 'Password reset email sent successfully.'})
            except Exception as e:
                print(f'Error sending email: {str(e)}')
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    return Response({'error': f'Maximum retry attempts reached. Failed to send email.'}, status=500)

    return Response(serializer.errors, status=400)

# Your existing reset_password_confirm view
@csrf_exempt
@require_POST
def reset_password_confirm(request, uidb64, token):
    print(f"Received token from URL: {token}")  # Add this line for debugging
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Valid token, allow the user to reset the password
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return JsonResponse(
                {"redirect_url": "http://localhost:3000/reset-password", "message": "Password reset successful."}
            )
        else:
            return JsonResponse(
                {"redirect_url": "http://localhost:3000/reset-password", "error": "Passwords do not match."},
                status=400,
            )

    return JsonResponse(
        {"redirect_url": "http://localhost:3000/Login", "error": "Invalid user or token."},
        status=400,
    )


@csrf_exempt
@require_POST
def update_password(request):
    # Assuming the request data is sent as JSON
    data = json.loads(request.body)

    # Extract user ID, new password, and confirm password from the request
    user_id_b64 = data.get("user_id")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    try:
        # Decode base64-encoded user ID
        user_id = force_str(urlsafe_base64_decode(user_id_b64))

        # Retrieve the user based on the user ID
        user = get_user_model().objects.get(pk=user_id)

        # Check if the new password matches the confirm password
        if new_password == confirm_password:
            # Validate the password using Django's built-in validators
            validate_password(new_password, user=user)

            # Reset the user's password
            user.set_password(new_password)
            user.save()

            return JsonResponse(
                {"redirect_url": "http://localhost:3000/Login", "message": "Password reset successful."},
            )
        else:
            return JsonResponse(
                {"redirect_url": "http://localhost:3000/reset-password", "error": "Passwords do not match."},
                status=400,
            )
    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"redirect_url": "http://localhost:3000/Login", "error": "User not found."},
            status=400,
        )
    except ValidationError as e:
        return JsonResponse(
            {"redirect_url": "http://localhost:3000/Login", "error": e.messages[0]},
            status=400,
        )

##########################################################################################

##############################################################################################

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Activation successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid activation link'}, status=400)


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})
###############################################################################################

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


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_rent(request):
#     customer_id = request.auth.payload.get("user_id")
#     rents = Rent.objects.filter(renter=customer_id)
#     serializer = RentSeriallizer(rents, many=True)
#     serialized_rents = serializer.data
#     return Response({"rents": serialized_rents}, status=status.HTTP_200_OK)


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


# @api_view(['GET'])
# def get_all_rents(request):
#     paginator = CustomPagination()
#     rents = Rent.objects.filter(is_deleted=False)
#     paginated_rents = paginator.paginate_queryset(rents, request)

#     serializer = RentSeriallizer(paginated_rents, many=True)
#     serialized_rents = serializer.data

#     return Response({"rents": serialized_rents}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def get_all_transactions(request):
    paginator = CustomPagination()
    transactions = Transaction.objects.filter(is_deleted=False)
    paginated_transactions = paginator.paginate_queryset(transactions, request)

    serializer = TransactionSeriallizer(paginated_transactions, many=True)
    serialized_transactions = serializer.data

    return Response({"transactions": serialized_transactions}, status=status.HTTP_200_OK)


def get_items_in_order(order_id):
    items = OrderItem.objects.filter(order_id=order_id)

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
        for orderitem in orderitems_data:
            product = Product.objects.get(id=orderitem['product_id'])
            if product.stock  < orderitem['quantity']:
                return Response({"msg": "Items is more than the stock"}, status=status.HTTP_400_BAD_REQUEST)

        # Create an Order instance
        order_serializer = OrderSeriallizer(data={'user': user_instance, 'status': 'Cancelled', 'total': 0,'is_deleted': False})
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
    order = Order.objects.get(pk=order_id,is_deleted=False)
    try:
        orderitems = OrderItem.objects.filter(order_id=order_id)
    except OrderItem.DoesNotExist:
        return Response({"msg":"can not find order items for this order"}, status=status.HTTP_400_BAD_REQUEST)
    seriallized_items = OrderItemSeriallizer(orderitems,many=True).data
    seriallized_order = OrderSeriallizer(order).data
    customer = User.objects.get(pk=order.user.user.id)
    customer_email = customer.email
    return Response({"seriallized_items":seriallized_items,"order":seriallized_order,"customer_email":customer_email},
                    status=status.HTTP_200_OK)


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
        order_items = OrderItem.objects.filter(order_id=order.id)
        for order_item in order_items:
            product = Product.objects.get(pk=order_item.product_id.id)
            product.stock -= order_item.quantity
            product.save()

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
        return Response({"msg": "Order created successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('new_status', None)

    if new_status is None or new_status not in dict(Order.STATUS_CHOICES).keys():
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Your logic to update the order status goes here
        order.status = new_status
        order.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = OrderSeriallizer(order)
    return Response({"order": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # You can add additional logic here to handle saving the order status to the database
    # For simplicity, let's assume you just want to return a success response

    return Response({"success": True}, status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# def delete_rent(request, rent_id):
#     rent_instance = get_object_or_404(Rent, id=rent_id)

#     if request.method == 'DELETE':
#         rent_instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#####################################################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transactions(request):
    customer_id = request.auth.payload.get('user_id')
    paginator = CustomPagination()
    transactions = Transaction.objects.filter(is_deleted=False,user=customer_id)
    paginated_transactions = paginator.paginate_queryset(transactions, request)
    serializer = TransactionSeriallizer(paginated_transactions, many=True)
    serialized_transactions = serializer.data
    return Response({"transactions": serialized_transactions}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_items_user(request):
    customer_id = request.auth.payload.get('user_id')
    order_id = request.GET.get('order_id')
    order = Order.objects.get(pk=order_id)
    if customer_id == order.user.user.id:
        try:
            orderitems = OrderItem.objects.filter(order_id=order_id)
        except OrderItem.DoesNotExist:
            return Response({"msg":"can not find order items for this order"}, status=status.HTTP_400_BAD_REQUEST)
        seriallized_items = OrderItemSeriallizer(orderitems,many=True).data
        seriallized_order = OrderSeriallizer(order).data
        customer = User.objects.get(pk=order.user.user.id)
        customer_email = customer.email
        return Response({"seriallized_items":seriallized_items,"order":seriallized_order,"customer_email":customer_email},
                        status=status.HTTP_200_OK)
    else:
        return Response(
            {"msg": "You are not validated to get this info."},
            status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    customer_id = request.auth.payload.get('user_id')
    customer = Customer.objects.get(pk=customer_id)
    try:
        orders = Order.objects.filter(user=customer.user.id, is_deleted=False)
    except Order.DoesNotExist:
        return Response({"msg":"you have no Orders"}, status=status.HTTP_200_OK)
    seriallized_orders = OrderSeriallizer(orders, many=True).data
    return Response(seriallized_orders,status=status.HTTP_200_OK)

@require_POST
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse({'message': 'Order deleted successfully'}),


def curr_user(request):
    user = request.user
    print(user.username)
    if user.is_authenticated:
        if user.is_superuser:
            # Redirect to the dashboard for admin users
            return None
        else:
            # For non-admin users, you can redirect to a different page or handle as needed
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'is_authenticated': True,
            })
    else:
        return JsonResponse({'is_authenticated': False})

def middleware_endpoint(request):
    # Simulate the middleware response
    response_data = {"redirect": reverse('index')}
    return JsonResponse(response_data)

