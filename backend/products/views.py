from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAdminUser
from .models import Product, ProductVariant, Future, ProductImages
from .serializers import ProductSerializer, ProductVariantSerializer, FutureSerializer, ProductImageSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:

            return [permissions.AllowAny()]
        elif self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:

            return [IsAdminUser()]
        return super().get_permissions()


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer


class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer


class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer
