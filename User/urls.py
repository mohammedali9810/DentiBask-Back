from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .api import OrderViewSet, OrderItemViewSet, ClinicViewSet, CustomerViewSet,RentViewSet,AddInfoViewSet,PayInfoViewSet

router = DefaultRouter()
router.register('order',OrderViewSet)
router.register('orderitem',OrderItemViewSet)
router.register('clinic',ClinicViewSet)
router.register('customer',CustomerViewSet)
router.register('rent',RentViewSet)
router.register('addinfo',AddInfoViewSet)
router.register('payinfo',PayInfoViewSet)


urlpatterns=[path('', include(router.urls)),]