from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (OrderViewSet, OrderItemViewSet, ClinicViewSet, CustomerViewSet, RentViewSet, AddInfoViewSet,
   PayInfoViewSet, MyObtainToken, check_email, register, activate_account,
                  add_clinic, get_user_clinic, get_all_clinics, delete_clinic, delete_user, get_csrf_token,userdata,update_customer)


router = DefaultRouter()
router.register('order', OrderViewSet)
router.register('orderitem', OrderItemViewSet)
router.register('clinic', ClinicViewSet)
router.register('customer', CustomerViewSet)
router.register('rent', RentViewSet)
router.register('addinfo', AddInfoViewSet)
router.register('payinfo', PayInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainToken.as_view(), name='token_obtain_pair'),
    path('checkemail/', check_email, name='check_email'),
    path('addclinic/', add_clinic, name='add_clinic'),
    path('userclinic/', get_user_clinic, name='get_user_clinic'),
    path('get_all_clinics/', get_all_clinics, name='get_all_clinic'),
    path('delete_clinic/', delete_clinic, name='delete_clinic'),
    path('delete_user/', delete_user, name='delete_user'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('register/', register, name='register'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
path('userdata/', userdata, name='userdata'),
path('update_customer/', update_customer, name='update_customer'),

]
