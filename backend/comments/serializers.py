from rest_framework import serializers
from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'product', 'author', 'body', 'created_at', 'like_count']
        read_only_fields = ['author', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'comment']
        read_only_fields = ['user']
