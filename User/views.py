# Create your views here.

# views.py

# from .token import account_activation_token
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
#
# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return JsonResponse({'message': 'Activation successful'})
#     else:
#         return JsonResponse({'error': 'Invalid activation link'}, status=400)

