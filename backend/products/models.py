from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from mptt.models import MPTTModel, TreeForeignKey


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(statuses=True)


class Category(MPTTModel):
    """Category model"""
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)

    statuses = models.BooleanField(
        default=True, verbose_name="آیا نمایش داده شود؟")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        # ordering = ['parent__id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class ProductGallery(models.Model):
    """Model to define product gallery images"""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, default=None)
    original_images = models.ImageField(upload_to='original_images/')
    resizes_images = ProcessedImageField(
        upload_to='resizes_images/', processors=[ResizeToFill(300, 400)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,)

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس ها")
        ordering = ['product']


COLOR_CHOICES = [
    ('blue', 'blue'),
    ('red', 'red'),
    ('white', 'white'),
    ('brown', 'brown'),
]
SIZE_CHOICES = [
    ('LARGE', 'LARGE'),
    ('MEDIUM', 'MEDIUM'),
    ('XLARGE', 'XLARGE'),
    ('XXLARGE', 'XXLARGE'),
]


class Product(models.Model):
    """Main model for products containing general information."""
    user = models.ForeignKey("accounts.CustomUser",
                             verbose_name=_("user"), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50,)
    slug = models.SlugField(unique=True)
    color = models.CharField(choices=COLOR_CHOICES, blank=False, max_length=50)
    size = models.CharField(choices=SIZE_CHOICES, blank=False, max_length=50)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, verbose_name=_(
        "Category"), on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    active = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='poster/',)
    view_count = models.ManyToManyField(
        IpAddress, through='MostViewed', blank=True, related_name='hits', verbose_name='بازدیدها')
    # promotion = models.ForeignKey("promotion.Promotion", verbose_name=_(
    #     "promotion"), on_delete=models.CASCADE)
    # loved =
    # rate = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class MostViewed(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    ip = models.ForeignKey(IpAddress,  on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)
