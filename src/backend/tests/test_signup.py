from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestSignUpAPI:
    url_signup = '/api/users/'

    def test_signup_with_no_data(self, client):
        """Проверка регистрации без ввода данных"""
        response = client.post(self.url_signup)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_signup}` не найден. Проверьте *urls.py*'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос на `{self.url_signup}`, не содержит данных, '
            'должен вернуться ответ со статусом 400'
        )

        response_json = response.json()
        empty_fields = [
            'email',
            'username',
            'password',
        ]
        for field in empty_fields:
            assert (
                field in response_json
                and isinstance(response_json.get(field), list)
            ), (
                f'Если в POST-запросе к `{self.url_signup}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях'
            )

    def test_signup_with_invalid_data(self, client, django_user_model):
        """Проверка регистрации с некорректными данными"""

        users_count = django_user_model.objects.count()
        invalid_data = {
            'email': 'not_email',
            'user': ' '
        }

        response = client.post(self.url_signup, data=invalid_data)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'некорректными данными не создаёт пользователя'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'некорректными данными возвращает статус 400'
        )

        response_json = response.json()
        invalid_fields = [
            'email',
            'username',
        ]
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.url_signup}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях'
            )

    def test_signup_with_valid_data(self, client, django_user_model):
        """Проверка регистрации с корректными данными"""
        users_count = django_user_model.objects.count()

        valid_data = {
            'email': 'vpupkin@yandex.ru',
            'username': 'vasya.pupkin',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'SomeTestPassword'
        }

        response = client.post(self.url_signup, data=valid_data)

        new_users_count = django_user_model.objects.count()
        assert users_count == (new_users_count - 1), (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'корректными данными создаёт пользователя'
        )

        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'корректными данными возвращает статус 201'
        )

        response_json = response.json()
        del valid_data['password']
        del response_json['id']
        assert response_json == valid_data, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'корректными данными возвращает ответ в соответствии '
            'со спецификацией'
        )

    def test_signup_with_not_unique_email_username(
            self, client, django_user_model
    ):
        """Проверка регистрации с данными уже сущ. пользователя"""
        valid_data = {
            'email': 'test@test.test',
            'username': 'testtest',
            'first_name': 'Тесть',
            'last_name': 'Тестов',
            'password': 'SomeTestPassword'
        }

        client.post(self.url_signup, data=valid_data)
        users_count = django_user_model.objects.count()
        response = client.post(self.url_signup, data=valid_data)
        new_users_count = django_user_model.objects.count()
        assert users_count == new_users_count, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'данными существующего пользователя не создаёт '
            'нового пользователя'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'данными существующего пользователя возвращает '
            'статус 400'
        )

        response_json = response.json()

        unique_fields = ['email', 'username']

        for field in unique_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.url_signup}` переданы '
                'данные существующего пользователя, в ответе должна '
                'возвращаться информация о необходимой'
                'уникальности полей'
            )
