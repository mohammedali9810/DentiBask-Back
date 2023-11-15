from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Product,Category
from .seriallizer import ProductSeriallizer, CategorySeriallizer
from rest_framework import viewsets, pagination, permissions, status
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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
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
        category_name = request.query_params.get('category', None)

        if category_name:
            category = get_object_or_404(Category, name=category_name)
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
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySeriallizer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


@api_view(['GET'])
def get_all_products(request):
    paginator = CustomPagination()
    products = Product.objects.all()
    paginated_products = paginator.paginate_queryset(products, request)

    # Serialize the paginated products
    serializer = ProductSeriallizer(paginated_products, many=True)
    serialized_products = serializer.data

    # Return the paginated response
    return paginator.get_paginated_response(serialized_products)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request):
    product_id = request.data.get('id')
    product = Product.objects.get(pk=product_id)
    product.name = request.data.get('title', product.name)
    product.price = request.data.get('price', product.price)
    product.desc = request.data.get('description', product.desc)
    categorry_id = request.data.get('categorry_id', product.Categ_id.id)
    category = get_object_or_404(Category, pk=categorry_id)
    product.Categ_id = category
    if 'image' in request.data and request.data['image'] and request.data['image'] != "":
        product.image = request.data['image']
    else:
        request.data['image'] = product.image
    try:
        product.full_clean()
        product.save()
        return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"msg": "Wrong data", "error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
