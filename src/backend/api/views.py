from asgiref.sync import async_to_sync
from django.conf import settings
from rest_framework import viewsets, permissions, status, mixins
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

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


class RandomUserCreateViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    def list(self, request):
        url = settings.RANDOM_USER_URL
        response = requests.get(url)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()['results'][0]

            User.objects.create(
                username=data['login']['username'],
                email=data['email'],
                first_name=data['name']['first'],
                last_name=data['name']['last'],
                password=data['login']['password']
            )

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Не удалось получить данные'},
                status=response.status_code
            )
