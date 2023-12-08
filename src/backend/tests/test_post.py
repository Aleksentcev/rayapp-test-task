from http import HTTPStatus

import pytest

from posts.models import Post


@pytest.mark.django_db(transaction=True)
class TestPostsAPI:

    posts_url = '/api/posts/'
    base_64_image = (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAA'
        'AABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK'
        '5CYII=='
    )

    def test_access_not_authenticated_posts_list(self, client):
        """
        Проверка существования эндпоинта posts/ доступа к нему
        неавторизованного пользователя
        """

        response = client.get(self.posts_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.posts_url}`. Проверьте *urls.py*.'
        )

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.posts_url}` возвращает код 200'
        )

    def test_posts_list(
            self, client,
            post_1, post_2,
            user, mock_media
    ):
        """Проверка корректности работы эндпоинта /posts/ для GET-запросов"""

        json_response = client.get(self.posts_url).json()

        assert json_response and isinstance(
            json_response, list
        ), (
            f'Проверьте, что в ответ на GET-запрос к `{self.posts_url}'
            ' находится список'
        )

        posts = json_response

        assert len(posts) == Post.objects.count(), (
            f'Проверьте, что в ответ на GET-запрос к `{self.posts_url}`'
            'в списке постов содержатся все посты'
        )

        post = posts[1]

        fields_types = {
            'id': int,
            'author': dict,
            'image': str,
            'text': str,
            'name': str,
        }

        for field, type in fields_types.items():
            assert field in post, (
                f'Проверьте, что в ответ на GET-запрос к `{self.posts_url}`'
                f'для каждого поста определено поле {field}'
            )

            assert isinstance(post[field], type), (
                f'Проверьте, что в ответ на GET-запрос к `{self.posts_url}`'
                f'для каждого поста поле {field} определяется типом {type}'
            )

    def test_access_not_authenticated_posts_detail(self, client, post_1):
        """
        Проверка существования эндпоинта posts/{pk} и наличия доступа к нему
        неавторизованного пользователя
        """
        pk = post_1.id
        post_detail_url = f'/api/posts/{pk}/'

        response = client.get(post_detail_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{post_detail_url}` не найден. Проверьте *urls.py*'
        )

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{post_detail_url}` возвращает код 200'
        )

    def test_post_detail(self, client, post_1, user):
        """
        Проверка корректности работы эндпоинта /posts/<id>/
        для GET-запросов
        """
        pk = post_1.id
        post_detail_url = f'/api/posts/{pk}/'

        json_response = client.get(post_detail_url).json()

        post = json_response

        fields_types = {
            'id': int,
            'author': dict,
            'image': str,
            'text': str,
            'name': str,
        }

        for field, type in fields_types.items():
            assert field in post, (
                f'Проверьте, что в ответ на GET-запрос к `{post_detail_url}`'
                f'для каждого поста определено поле {field}'
            )

            assert isinstance(post[field], type), (
                f'Проверьте, что в ответ на GET-запрос к `{post_detail_url}`'
                f'для каждого поста поле {field} определяется типом {type}'
            )

    def test_access_not_authenticated_post_create_url(self, client):
        """
        Проверка наличия доступа к эндпоинту созданию поста
        неваторизованного пользователя
        """
        response = client.post(self.posts_url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            f'`{self.posts_url}` возвращает код 401'
        )

    def test_post_create_with_no_data(self, user_client):
        response = user_client.post(self.posts_url)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что POST-запрос к `{self.posts_url}` '
            'без данных возвращает код 400'
        )

        response_json = response.json()

        required_fields = [
            'name',
            'text',
            'image',
        ]
        for field in required_fields:
            assert field in response_json, (
                'Проверьте, что в ответе на POST-запрос к '
                f'`{self.posts_url}` без данных возвращается'
                f'список необходимых полей. Поле {field} должно '
                'быть в списке'
            )

    def test_post_create_with_invalid_data(self, user_client, mock_media):
        """
        Проверка, что POST-запрос с некорректными данными к эндпоинту posts/
        не создаёт пост
        """
        posts_count = Post.objects.count()
        invalid_data = {
            'text': ' ',
            'name': 1
        }
        response = user_client.post(self.posts_url, data=invalid_data)

        assert Post.objects.count() == posts_count, (
            'Проверьте, что POST-запрос с '
            'некорректными данными не создаёт пост'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что при POST-запросе с '
            'некорректными данными возвращается статус 400'
        )

    def test_post_create_with_valid_data(self, user_client, mock_media):
        """
        Проверка, что POST-запрос с корректными данными к эндпоинту posts/
        создаёт пост
        """
        posts_count = Post.objects.count()
        valid_data = {
            'name': 'string',
            'text': 'string',
            'image': self.base_64_image,
        }
        response = user_client.post(self.posts_url, data=valid_data)

        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что POST-запрос к `{self.posts_url}` '
            'с корректными данными возвращает код 201'
        )

        assert Post.objects.count() == posts_count + 1, (
            f'Проверьте, что POST-запрос к `{self.posts_url}` '
            'с корректными данными создаёт пост в базе данных'
        )

    def test_delete_post_by_author(self, user_client, post_1, mock_media):
        """Проверяет, что автор поста может его удалить"""
        pk = post_1.id
        delete_post_url = f'/api/posts/{pk}/'
        posts_count = Post.objects.count()
        response = user_client.delete(delete_post_url)

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос автора поста к '
            f'`{self.posts_url}` возвращает код 204'
        )

        assert Post.objects.count() == posts_count - 1, (
            'Проверьте, что DELETE-запрос автора поста к '
            f'`{self.posts_url}` удаляет пост'
        )

    def test_delete_post_not_by_author(
        self, another_user_client, post_1, mock_media
    ):
        """
        Проверяет, что авторизованный пользователь может
        удалять только свои посты
        """
        pk = post_1.id
        delete_post_url = f'/api/posts/{pk}/'
        posts_count = Post.objects.count()
        response = another_user_client.delete(delete_post_url)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос автора поста к '
            f'`{self.posts_url}` возвращает код 403'
        )

        assert Post.objects.count() == posts_count, (
            'Проверьте, что DELETE-запрос не автора поста к '
            f'`{self.posts_url}` не удаляет пост'
        )
