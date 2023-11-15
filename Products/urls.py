from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .api import (ProductViewSet, CategoryViewSet, get_csrf_token
,get_all_products,update_product,get_categories,products_catgory,product_detail)

router = DefaultRouter()
router.register(r'products',ProductViewSet)
router.register(r'category',CategoryViewSet)

urlpatterns=[path('', include(router.urls)),path('get_csrf_token/',get_csrf_token)
                ,path('get_products/',get_all_products)
                ,path('update_product/',update_product)
                ,path('get_categories/',get_categories,name='get_categories')
                ,path('products_catgory/',products_catgory,name='products_catgory')
                ,path('product_detail/',product_detail,name='product_detail')

]
