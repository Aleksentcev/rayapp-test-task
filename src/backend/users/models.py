from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    email = models.EmailField(
        'Адрес эл.почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')],
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
