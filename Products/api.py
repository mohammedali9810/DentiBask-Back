from django.shortcuts import get_object_or_404
from .models import Product,Category
from .seriallizer import ProductSeriallizer, CategorySeriallizer
from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from django.middleware.csrf import get_token
from django.http import JsonResponse


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

class CustomPagination(pagination.PageNumberPagination):
    page_size = 12  # Number of items per page
    page_size_query_param = 'page_size'  # Allows clients to change the page size by providing a query parameter
    max_page_size = 1000  # Maximum number of items that can be requested per page

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSeriallizer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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
    def list(self, request, *args, **kwargs):
        category_name = request.query_params.get('name', None)

        if category_name:
            category = get_object_or_404(Category, name=category_name)
            #ToDo
            # take the name of category and find the id of that name catgory from Catgorey model
            category_id = category.id  # Get the ID of the category
            queryset = Product.objects.filter(Categ_id=category_id)
      
            queryset = Product.objects.filter(Categ_id=category)
        else:
            queryset = Product.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name:
            return Product.objects.filter(name__icontains=name)
        return Product.objects.all()
    
    def retrieve_by_id(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySeriallizer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]