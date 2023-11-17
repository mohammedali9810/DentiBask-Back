from rest_framework import serializers
from .models import Product, Category

class CategorySeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['is_deleted']

class ProductSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['is_deleted']
    def create(self, validated_data):
        # Exclude 'is_deleted' from the data sent during creation
        validated_data.pop('is_deleted', None)
        return super().create(validated_data)

