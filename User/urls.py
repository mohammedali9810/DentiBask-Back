from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (OrderViewSet, OrderItemViewSet, ClinicViewSet, CustomerViewSet, RentViewSet, AddInfoViewSet,
   PayInfoViewSet, MyObtainToken, check_email, register, activate_account,
                  add_clinic, get_user_clinic, get_all_clinics, delete_clinic, delete_user, get_csrf_token,userdata,update_customer
,get_all_orders,get_user_order,get_user_rent,get_all_rents,get_user_transaction,get_all_transactions,get_items_in_order
                  ,create_order,change_order_status,save_order_status,delete_rent)


router = DefaultRouter()
router.register('order', OrderViewSet)
router.register('orderitem', OrderItemViewSet)
router.register('clinic', ClinicViewSet)
router.register('customer', CustomerViewSet)
router.register('rent', RentViewSet)
router.register('addinfo', AddInfoViewSet)
router.register('payinfo', PayInfoViewSet)
router.register('transaction', TransactionViewSet)

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
    path('userorder/', get_user_order, name='get_user_order'),
    path('get_all_orders/', get_all_orders, name='get_all_orders'),

    path('userrent/', get_user_rent, name='get_user_rent'),
    path('get_all_rents/', get_all_rents, name='get_all_rents'),

    path('usertransaction/', get_user_transaction, name='get_user_transaction'),
    path('get_all_transactions/', get_all_transactions, name='get_all_transactions'),

    path('get_items_in_order/', get_items_in_order, name='get_items_in_order'),

    path('userdata/', userdata, name='userdata'),
    path('orders/<int:order_id>/change_status/', change_order_status, name='change_order_status'),
    path('orders/<int:order_id>/save_status/', save_order_status, name='save_order_status'),

    path('api/rents/<int:rent_id>/', delete_rent, name='delete_rent'),

    path('update_customer/', update_customer, name='update_customer'),
    path('create_order/', create_order, name='create_order'),
]
