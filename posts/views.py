from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from posts.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Create your views here.
