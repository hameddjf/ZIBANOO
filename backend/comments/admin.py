from django.contrib import admin
from .models import Comment, Like


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'body', 'created_at', 'like_count')
    search_fields = ('author__username', 'body')
    list_filter = ('created_at',)


    def like_count(self, obj):
        return obj.likes.count()


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    search_fields = ('user__username', 'comment__body')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
