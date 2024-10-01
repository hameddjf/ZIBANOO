from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Tag, Brand


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def get_prepopulated_fields(self, request, obj=None):
        return self.prepopulated_fields


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin interface for managing Brands."""
    list_display = ('name', 'slug', 'created_at',
                    'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """Override to add filters or modify the queryset."""
        return super().get_queryset(request).order_by('-created_at')
