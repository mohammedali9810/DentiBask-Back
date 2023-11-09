from .models import Product,Category
from .seriallizer import ProductSeriallizer, CategorySeriallizer
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSeriallizer
    lookup_field = 'pk'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySeriallizer
    lookup_field = 'pk'



