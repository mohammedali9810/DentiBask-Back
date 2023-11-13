from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet, CategoryViewSet, get_csrf_token

router = DefaultRouter()
router.register(r'products',ProductViewSet)
router.register(r'category',CategoryViewSet)

urlpatterns=[path('', include(router.urls)),path('get_csrf_token/',get_csrf_token)]