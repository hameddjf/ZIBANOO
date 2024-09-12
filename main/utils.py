import re
from django.utils.text import slugify as django_slugify


def get_client_ip(request):
    """Get the client's IP address from the HTTP request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
