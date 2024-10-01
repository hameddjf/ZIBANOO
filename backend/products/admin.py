import admin_thumbnails

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductVariant, Future, ProductImages

# Register your models here.


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin panel for managing Product Variants"""
    list_display = ('get_product_name', 'get_product_image',
                    'price', 'discount_price', 'stock', 'sold')
    search_fields = ('product__name', 'price')
    list_filter = ('product',)

    fieldsets = (
        (None, {
            'fields': ('product', 'price', 'discount_price', 'stock', 'sold')
        }),
        # فیلد تصویر به اینجا نیازی نیست
    )

    @admin.display(description=_('Product Name'))
    def get_product_name(self, obj):
        return obj.product.name  # نام محصول را برمی‌گرداند

    @admin.display(description=_('Product Image'))
    def get_product_image(self, obj):
        if obj.product.poster:  # بررسی می‌کند که آیا obj.product.poster موجود است یا خالی نیست
            return format_html(
                '<img src="{}" style="width:55px;height:55px;"/>', obj.product.poster.url
            )
        return "-"


@admin.register(Future)
class FutureAdmin(admin.ModelAdmin):
    """Admin panel for managing Future (features)"""
    list_display = ('key', 'value')
    search_fields = ('key', 'value')

    fieldsets = (
        (None, {
            'fields': ('key', 'value')
        }),
    )


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    """Admin panel for managing Product Images"""
    list_display = ('id', 'image_thumbnail')
    search_fields = ('image_thumbnail',)

    @admin.display(description=_('Thumbnail Image'))
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:55px;height:55px;"/>', obj.image.url
            )
        return "-"


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin panel for managing Products"""
    list_display = ('name', 'image_thumbnail', 'category',
                    'brand', 'view_count', 'like_count', 'created_at')
    search_fields = ('name', 'category__name', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    inlines = [ProductImagesInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'brand', 'slug', 'description')
        }),
        ('Media', {
            'classes': ('collapse',),
            'fields': ('poster',),  # فیلد تصویری اصلی
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count', 'created_at'),
        }),
    )

    @admin.display(description=_('Thumbnail Image'))
    def image_thumbnail(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:55px;height:55px;"/>', obj.poster.url
            )
        return "-"
