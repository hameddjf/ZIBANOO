# views.py
from rest_framework import viewsets
from .models import Product, ProductImages, ProductVariant, Future
from .serializers import ProductSerializer, ProductImagesSerializer, ProductVariantSerializer, FutureSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]


class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer
    permission_classes = [IsAdminOrReadOnly]
