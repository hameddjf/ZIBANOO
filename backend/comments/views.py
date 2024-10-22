from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Comment, Like
from .serializers import CommentSerializer, LikeSerializer


class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user:
            return Response({"detail": "You do not have permission to edit this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user:
            return Response({"detail": "You do not have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeCreateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if Like.objects.filter(user=request.user, comment=comment).exists():
            return Response({"detail": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=request.user, comment=comment)
        return Response({"detail": "Liked the comment."}, status=status.HTTP_201_CREATED)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = Like.objects.filter(user=request.user, comment=comment).first()
        if like:
            like.delete()
            return Response({"detail": "Unliked the comment."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You haven't liked this comment."}, status=status.HTTP_400_BAD_REQUEST)
