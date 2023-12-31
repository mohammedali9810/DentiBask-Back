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
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
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
    products = Product.objects.filter(is_deleted=False)
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSeriallizer(paginated_products, many=True)
    serialized_products = serializer.data
    return paginator.get_paginated_response(serialized_products)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request):
    product_id = request.data.get('id')
    product = Product.objects.get(pk=product_id)
    product.name = request.data.get('title', product.name)
    product.price = request.data.get('price', product.price)
    product.desc = request.data.get('description', product.desc)
    product.stock = request.data.get('stock',product.stock)
    product.unit = request.data.get('unit',product.unit)
    categorry_id = request.data.get('categorry_id', product.Categ_id.id)
    category = get_object_or_404(Category, pk=categorry_id)
    product.Categ_id = category
    try:
        if 'image' in request.data and request.data['image']:
            # Access the name attribute of the InMemoryUploadedFile object
            image_name = request.data['image']

            # Check if the image name starts with the specified URL
            if image_name.startswith('https://dentibaskbucket.s3.amazonaws.com/images/product/'):
                product.full_clean()
                product.save()
                # If the image name starts with the specified URL, do not update it
                return Response({"msg": "Data has been modified and no image added"}, status=status.HTTP_200_OK)
            else:
                # If the image name doesn't start with the specified URL, update the category's image
                product.image = request.data['image']
                product.full_clean()
                product.save()
    except KeyError:
        # Handle the case where 'image' key is not present in the request data
        return Response({"msg": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


    try:
        product.full_clean()
        product.save()
        return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"msg": "Wrong data", "error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)



    ########################################################################

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.filter(is_deleted=False)
    seriallized_categories = CategorySeriallizer(categories,many=True).data
    return Response(seriallized_categories,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_category_products(request):
    category_id = request.GET.get('category_id')
    try:
        products = Product.objects.filter(Categ_id=category_id)
    except Product.DoesNotExist:
        return Response({"msg":"Can not find products"}, status=status.HTTP_400_BAD_REQUEST)
    seriallized_products = ProductSeriallizer(products,many=True).data
    return Response(seriallized_products,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_product(request):
    try:
        serialized_product = ProductSeriallizer(data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response({"msg": "Product added successfully"}, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        print("Validation Error:", e.message_dict)
        return Response({"msg": "Wrong data", "error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        print("Exception during save:", str(e))
        traceback.print_exc()
        return Response({"msg": "Internal Server Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_product(request):
    product_id = request.GET.get('product_id')
    print(product_id)
    try:
        product = Product.objects.get(pk=product_id)
    except Category.DoesNotExist:
        return Response({"msg": " Product not found"}, status=status.HTTP_400_BAD_REQUEST)
    product.is_deleted = True
    product.save()
    return Response({"msg": " Category deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_category(request):
    category_id = request.GET.get('category_id')
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({"msg": " Category not found"}, status=status.HTTP_400_BAD_REQUEST)
    category.is_deleted = True
    category.save()
    return Response({"msg": " Category deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_category(request):
    category_id = request.data.get('category_id')
    category = Category.objects.get(pk=category_id)
    category.name = request.data.get('name', category.name)
    category.desc = request.data.get('desc', category.desc)

    try:
        if 'image' in request.data and request.data['image']:
            # Access the name attribute of the InMemoryUploadedFile object
            image_name = request.data['image']

            if image_name.startswith('https://dentibaskbucket.s3.amazonaws.com/images/category/'):
                category.full_clean()
                category.save()
                return Response({"msg": "Data has been modified and no image added"}, status=status.HTTP_200_OK)
            else:
                category.image = request.data['image']
    except KeyError:
        # Handle the case where 'image' key is not present in the request data
        return Response({"msg": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category.full_clean()
        category.save()
        return Response({"msg": "Data has been modified"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"msg": "Wrong data", "error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def products_catgory(request):
    category_name = request.query_params.get('name', None)

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        queryset = Product.objects.filter(Categ_id=category.id)
    else:
        queryset = Product.objects.all()

    serializer = ProductSeriallizer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request):
    pk = request.query_params.get('id')

    if pk is None:
        return Response({'error': 'Product ID (pk) is required in the query parameters.'},
                        status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSeriallizer(product)
    return Response(serializer.data)


@api_view(['GET'])
def product_search(request):
    name = request.query_params.get('name', None)

    if name:
        queryset = Product.objects.filter(name__icontains=name)
    else:
        queryset = Product.objects.all()

    serializer = ProductSeriallizer(queryset, many=True)
    return Response(serializer.data)
