from rest_framework import viewsets, permissions
from djoser.views import UserViewSet

from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import CustomUserSerializer, PostSerializer
from posts.models import Post, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrReadOnly,
    )

    def get_queryset(self):
        return Post.objects.select_related('author').all()
