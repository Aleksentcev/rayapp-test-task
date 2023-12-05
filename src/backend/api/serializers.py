import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from posts.models import Post, User


class CustomUserSerializer(UserSerializer):
    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )
        model = User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = (
            'username',
            'id',
            'password',
            'email',
            'first_name',
            'last_name',
        )
        model = User


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
        )
        model = Post
