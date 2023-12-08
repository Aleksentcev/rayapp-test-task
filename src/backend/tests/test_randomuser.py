import pytest
from rest_framework import status
from unittest.mock import patch


@pytest.mark.django_db(transaction=True)
class TestRandomAPI():
    random_url = '/api/random/'

    def test_random_user_create(self, client, django_user_model):
        """
        Проверка доступа к randomuser и создания пользователя из
        полученных данных
        """

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = status.HTTP_200_OK
            mock_get.return_value.json.return_value = {
                'results': [{
                    'login': {
                        'username': 'testuser', 'password': 'password123'
                    },
                    'email': 'test@example.com',
                    'name': {'first': 'Test', 'last': 'User'}
                }]
            }

            response = client.get(self.random_url)

        assert response.status_code == status.HTTP_200_OK, (
            f'Проверьте, что GET-запрос к `{self.random_url}` '
            'возвращает статус 200'
        )

        mock_get.assert_called_once_with('https://randomuser.me/api/')

        assert django_user_model.objects.filter(
            username='testuser'
        ).exists(), (
            f'Проверьте, что GET-запрос к `{self.random_url}` создает нового '
            'пользователя'
        )
