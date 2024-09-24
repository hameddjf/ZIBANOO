from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)  # شماره تلفن به فرم اضافه می‌کنیم

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("این یوزرنیم قبلاً ثبت شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone_number=phone).exists():  # تغییر به phone_number
            raise forms.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return phone


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone_number']


# فرم لاگین
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=255, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)


# فرم تغییر پسورد
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
