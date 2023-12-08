from asgiref.sync import async_to_sync
from rest_framework import viewsets, permissions, status
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import CustomUserSerializer, PostSerializer
from posts.models import Post, User
from .utils import process_text_async


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

    @action(detail=True, methods=['post'])
    def process_text(self, request, pk=None):
        post = self.get_object()
        text = post.text

        if text:
            processed_text = async_to_sync(process_text_async)(text)
            post.text = processed_text
            post.save()
            serialized_post = self.get_serializer(post)
            return Response(
                serialized_post.data, status=status.HTTP_201_CREATED
            )

        return Response(
            {'error': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST
        )
