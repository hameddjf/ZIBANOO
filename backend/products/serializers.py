from django.db.models import Count
from rest_framework import serializers
from .models import IpAddress, Category, ProductGallery, Product, MostViewed


class CategorySerializer(serializers.ModelSerializer):
    """serializer for Category"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'statuses', 'children']

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data


class ProductGallerySerializer(serializers.ModelSerializer):
    """serializer for ProductGallery"""
    class Meta:
        model = ProductGallery
        fields = ['id', 'resizes_images']


class ProductSerializer(serializers.ModelSerializer):
    """product serialaaizer for home & store page"""
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'color', 'size', 'price', 'stock', 'sold',
                  'description', 'category', 'created', 'updated', 'active',
                  'poster', 'images', 'view_count']
        read_only_fields = ['created', 'updated', 'sold', 'view_count']

    def get_images(self, obj):
        return ProductGallerySerializer(obj.images).data['resizes_images']

    def get_view_count(self, obj):
        return MostViewed.objects.filter(product=obj).count()

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("موجودی نمی‌تواند منفی باشد.")
        return value


class ProductDetailSerializer(ProductSerializer):
    """product serialaaizer for single page"""

    most_viewed = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['most_viewed']

    def get_most_viewed(self, obj):
        most_viewed = MostViewed.objects.filter(product=obj) \
            .values('user') \
            .annotate(view_count=Count('id')) \
            .order_by('-view_count')[:5]
        return [{'user_id': item['user'], 'view_count': item['view_count']} for item in most_viewed]
