from django.urls import path

from .views import SignUpView, ActivateAccountView, CustomLoginView, CustomLogoutView, ProfileUpdateView

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/signup/', SignUpView.as_view(), name='signup_api'),
    path('api/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('api/login/', CustomLoginView.as_view(), name='login_api'),
    path('api/logout/', CustomLogoutView.as_view(), name='logout_api'),
    path('api/profile/', ProfileUpdateView.as_view(), name='profile_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # دریافت توکن JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # رفرش توکن JWT
]
