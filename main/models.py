from django.db import models

# Create your models here.


class Base(models.Model):

    title = models.CharField(max_length=50,)
    content = models.TextField()
    slug = models.SlugField()

    category = models.ManyToManyField("app.Model", verbose_name=_(""))
    tags = models.ManyToManyField("app.Model", verbose_name=_(""))
    user = models.ForeignKey(
        "app.Model", verbose_name=_(""), on_delete=models.CASCADE)

    is_published = models.BooleanField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
