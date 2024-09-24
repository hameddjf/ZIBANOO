from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import CustomLoginForm, CustomPasswordChangeForm
from django.views.generic import UpdateView, TemplateView
from .models import CustomUser
from .tokens import account_activation_token
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout


class EmailConfirmationView(LoginRequiredMixin,TemplateView):
    login_url = 'signup'
    template_name = 'registration/email_confirmation.html'

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('email_confirmation')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # ارسال ایمیل فعال‌سازی
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        link = reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token})
        activate_url = f"http://{domain}{link}"
        email_subject = 'Activate your account'
        email_body = f'Please click the link to activate your account: {activate_url}'
        send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])

        return redirect('email_confirmation')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            # چک کردن اینکه آیا توکن منقضی شده یا نه
            token_created_at = user.date_joined.timestamp()
            if account_activation_token.is_token_expired(user, token_created_at):
                return render(request, 'activation_invalid.html', {'message': 'لینک فعال‌سازی منقضی شده است'})

            # اگر توکن معتبر باشد و منقضی نشده باشد
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return render(request, 'activation_invalid.html', {'message': 'لینک فعال‌سازی منقضی شده است'})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')


class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        print("outed login1")
        return redirect('login')

    def post(self, request, *args, **kwargs):
        logout(request)
        print("outed login2")
        return redirect('login')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
