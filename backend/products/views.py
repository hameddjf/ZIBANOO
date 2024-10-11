from django.db.models import Count, Subquery, OuterRef, OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, MostViewed
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()

        # view count product
        view_count_subquery = MostViewed.objects.filter(product=OuterRef('pk')) \
            .values('product') \
            .annotate(count=Count('id')) \
            .values('count')

        queryset = queryset.annotate(view_count=Subquery(view_count_subquery))

        if self.action in ['list', 'home', 'shop']:
            queryset = queryset.only(
                'id', 'title', 'slug', 'price', 'poster', 'view_count')
        elif self.action in ['retrieve', 'single']:
            queryset = queryset.prefetch_related(
                Prefetch('images', queryset=ProductGallery.objects.only(
                    'resizes_images'))
            ).select_related('category')

        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'single']:
            return ProductDetailSerializer
        return ProductSerializer

    @action(detail=False)
    def home(self, request):
        """home page for product"""
        featured_products = self.get_queryset().filter(
            active=True).order_by('-view_count')[:5]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def shop(self, request):
        """store page for products"""
        products = self.get_queryset().filter(active=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def single(self, request, slug=None):
        """single page for product"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
