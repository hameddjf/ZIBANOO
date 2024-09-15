from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff')

    class Meta:
        model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
