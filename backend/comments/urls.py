from django.urls import path
from .views import CommentListCreateAPIView, CommentDetailAPIView, LikeCreateDestroyAPIView

urlpatterns = [
    path('', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('<int:comment_id>/like/', LikeCreateDestroyAPIView.as_view(), name='like-comment'),
]
