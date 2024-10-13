# serializers.py
from rest_framework import serializers
from .models import Product, ProductImages, ProductVariant, Future

class FutureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Future
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    future = FutureSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImagesSerializer(many=True, source='productimages_set', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
