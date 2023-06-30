from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from django.contrib.auth.hashers import make_password


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get("password")
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)

        
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.is_private and request.user != instance.owner:
            return Response({"detail": "You are not allowed to access this post."}, status=403)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return Response({"detail": "You are not allowed to update this post."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return Response({"detail": "You are not allowed to delete this post."}, status=403)
        return super().destroy(request, *args, **kwargs)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        user_id = request.data.get("user")
        post = Post.objects.filter(pk=post_id).first()
        if post is None:
            return Response({"detail": "Invalid post ID."}, status=400)
        if post.is_private and request.user != post.owner:
            return Response({"detail": "You are not allowed to like this post."}, status=403)
        like = Like.objects.filter(post=post, user_id=user_id).first()
        if like is not None:
            return Response({"detail": "You have already liked this post."}, status=400)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            return Response({"detail": "You are not allowed to update this like."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            return Response({"detail": "You are not allowed to delete this like."}, status=403)
        return super().destroy(request, *args, **kwargs)
