from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, ProductImages, ProductVariant, Future
from .serializers import ProductSerializer, ProductImagesSerializer, ProductVariantSerializer, FutureSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Product created successfully!', 'data': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Product updated successfully!', 'data': response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Product deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Product image uploaded successfully!', 'data': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Product image updated successfully!', 'data': response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Product image deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Product variant created successfully!', 'data': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Product variant updated successfully!', 'data': response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Product variant deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class FutureViewSet(viewsets.ModelViewSet):
    queryset = Future.objects.all()
    serializer_class = FutureSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Feature created successfully!', 'data': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'message': 'Feature updated successfully!', 'data': response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Feature deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
