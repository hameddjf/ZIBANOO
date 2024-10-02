from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductVariantViewSet, FutureViewSet, ProductImagesViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'futures', FutureViewSet)
router.register(r'images', ProductImagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
