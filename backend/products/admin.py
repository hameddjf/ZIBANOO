
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count

from .models import Category, Product, ProductGallery, IpAddress, MostViewed

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'status', 'product_count')
    list_filter = ('status', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['make_active', 'make_inactive']

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = _('Products Count')

    @admin.action(description=_('فعال کردن'))
    def make_active(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, _(
            f'{updated} categor{"y was" if updated ==
                                1 else "ies were"} successfully marked as active.'
        ))

    @admin.action(description=_('غیر فعال کردن'))
    def make_inactive(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, _(
            f'{updated} categor{"y was" if updated ==
                                1 else "ies were"} successfully marked as inactive.'
        ))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_thumbnail', 'category',
                    'price', 'stock', 'sold', 'active')
    list_filter = ('active', 'category', 'created', 'updated')
    search_fields = ('title', 'description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated', 'sold')
    actions = ['make_active', 'make_inactive']

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'slug', 'category', 'description')
        }),
        (_('Product Details'), {
            'fields': ('color', 'size', 'price', 'stock', 'sold')
        }),
        (_('Media'), {
            'classes': ('collapse',),
            'fields': ('poster', 'images')
        }),
        (_('Status and Statistics'), {
            'fields': ('active', 'created', 'updated')
        }),
    )

    @admin.display(description=_('Thumbnail'))
    def image_thumbnail(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;"/>',
                obj.poster.url
            )
        return "-"

    @admin.action(description=_('فعال کردن'))
    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, _(
            f'{updated} product{"" if updated ==
                                1 else "s"} successfully marked as active.'
        ))

    @admin.action(description=_('غیر فعال کردن'))
    def make_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, _(
            f'{updated} product{"" if updated ==
                                1 else "s"} successfully marked as inactive.'
        ))


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_image_preview', 'resized_image_preview')

    @admin.display(description=_('Original Image'))
    def original_image_preview(self, obj):
        if obj.original_images:
            return format_html(
                '<img src="{}" style="width:100px;height:100px;object-fit:cover;"/>',
                obj.original_images.url
            )
        return "-"

    @admin.display(description=_('Resized Image'))
    def resized_image_preview(self, obj):
        if obj.resizes_images:
            return format_html(
                '<img src="{}" style="width:100px;height:100px;object-fit:cover;"/>',
                obj.resizes_images.url
            )
        return "-"


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'views_count')
    search_fields = ('ip_address',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _views_count=Count('mostviewed', distinct=True),
        )
        return queryset

    def views_count(self, obj):
        return obj._views_count
    views_count.admin_order_field = '_views_count'
    views_count.short_description = _('Views Count')


@admin.register(MostViewed)
class MostViewedAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip', 'Created')
    list_filter = ('Created', 'product', 'user')
    date_hierarchy = 'Created'
    search_fields = ('product__title', 'user__username', 'ip__ip_address')
