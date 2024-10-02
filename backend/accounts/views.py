from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import CustomUserSerializer, LoginSerializer, CustomUserChangeSerializer
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


# from ratelimit.decorators import ratelimit


class SignUpView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        # ابتدا داده‌های ورودی کاربر را به serializer داده و اعتبارسنجی کنید
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # بررسی وجود کاربری با ایمیل یا شماره تلفن
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')  # Assuming phone_number field exists
        username = serializer.validated_data.get('username')

        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({'message': 'User with this phone number already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'message': 'User with this username already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # اگر کاربری با این ایمیل یا شماره تلفن وجود نداشت، ادامه دهید و کاربر را ثبت کنید
        user = serializer.save(is_active=False)  # Initially, user is inactive
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        activate_url = f"http://{domain}{reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token})}"
        email_subject = 'Activate your account'
        email_body = f'Please click the link to activate your account: {activate_url}'

        try:
            send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception as e:
            user.delete()  # Optionally delete user if email fails
            return Response({'message': 'Error sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'User registered successfully. Please check your email to activate your account.'},
                        status=status.HTTP_201_CREATED)


class ActivateAccountView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)  # Auto-login after activation
            refresh = RefreshToken.for_user(user)  # Generate JWT upon activation
            return Response({
                'message': 'Account activated and logged in successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Activation link is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # @ratelimit(key='ip', rate='5/m', block=True)  # Limit to 5 requests per minute
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'message': 'Account is not activated.'}, status=status.HTTP_403_FORBIDDEN)

        if user.check_password(password):
            login(request, user)
            refresh = RefreshToken.for_user(user)  # JWT token generation
            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)


class CustomPasswordChangeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserChangeSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.validated_data['new_password'] != serializer.validated_data['confirm_password']:
            return Response({'message': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
