from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'username', 'phone_number')


    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('username', 'phone_number', 'address', 'postal_code', 'note')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),  # اضافه کردن در حالت فقط خواندنی
    )

admin.site.register(CustomUser, CustomUserAdmin)
