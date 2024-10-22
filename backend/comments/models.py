from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from products.models import Product



class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.product}'

    @property
    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user} liked {self.comment}'
