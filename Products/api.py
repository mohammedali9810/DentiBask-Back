from .models import Product,Category
from .seriallizer import ProductSeriallizer, CategorySeriallizer
from rest_framework import viewsets, pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 12  # Number of items per page
    page_size_query_param = 'page_size'  # Allows clients to change the page size by providing a query parameter
    max_page_size = 1000  # Maximum number of items that can be requested per page


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        mutable_data = request.data.copy()
        if 'image' not in mutable_data or not mutable_data['image']:
            mutable_data['image'] = instance.image
        serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySeriallizer
    lookup_field = 'pk'
