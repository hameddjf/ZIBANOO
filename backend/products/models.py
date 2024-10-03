from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


from tags.models import Base
# Create your models here.


class Future(models.Model):
    """Model to define specific features of a product."""
    FUTURE_CHOICES = [
        ('color', 'color'),
        ('size', 'size'),
    ]
    key = models.CharField(choices=FUTURE_CHOICES, max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("ویژگی")
        verbose_name_plural = _("ویژگی ها")


class Product(Base):
    """Main model for products containing general information."""
    description = models.TextField(blank=True,)
    view_count = models.PositiveIntegerField(default=0,)
    like_count = models.PositiveIntegerField(default=0,)

    category = models.ForeignKey("tags.Category", verbose_name=_(
        "Category"), on_delete=models.CASCADE)
    brand = models.ForeignKey("tags.Brand", verbose_name=_(
        "brand"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def increment_view_count(self):
        self.view_count = F('view_count') + 1
        self.save()

    def like(self):
        self.like_count = F('like_count') + 1
        self.save()


class ProductImages(models.Model):
    """Model to store images of products."""
    product = models.ForeignKey(
        Product, verbose_name=_("productimages"), on_delete=models.CASCADE, default=None)
    image = models.ImageField(
        upload_to='images/', height_field=None, width_field=None, max_length=None, default=None)

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس ها")


class ProductVariant(models.Model):
    """Model to define different variants of a product"""
    product = models.ForeignKey(
        Product, related_name='variants', on_delete=models.CASCADE)
    future = models.ManyToManyField(Future, verbose_name=_("future"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0,)
    sold = models.IntegerField(default=0,)

    class Meta:
        verbose_name = _("ویژگی محصول")
        verbose_name_plural = _("ویژگی‌های محصولات")

    def __str__(self):
        futures = ', '.join([f.key for f in self.future.all()])
        return f"{self.product.name} - {futures}"
