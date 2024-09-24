from django.urls import path
from .views import SignUpView, ActivateAccountView, CustomLoginView, CustomLogoutView, CustomPasswordChangeView, \
    ProfileUpdateView, EmailConfirmationView, HomeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('email_confirmation/', EmailConfirmationView.as_view(), name='email_confirmation'),
    path('home/', HomeView.as_view(), name='home'),
]
