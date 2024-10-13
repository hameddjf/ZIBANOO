
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    اجازه دسترسی فقط برای ادمین‌ها (دسترسی کامل)، و کاربران عادی فقط اجازه مشاهده دارند.
    """

    def has_permission(self, request, view):
        # اگر درخواست فقط برای خواندن است (GET, HEAD, OPTIONS)، اجازه می‌دهد
        if request.method in permissions.SAFE_METHODS:
            return True
        # اگر کاربر ادمین است اجازه می‌دهد
        return request.user.is_staff
