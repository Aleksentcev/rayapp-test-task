![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 

# Тестовое задание от [ray.app](https://ray.app/) 

### Как запустить проект в контейнерах локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Aleksentcev/rayapp-test-task.git
```

```
cd rayapp-test-task/src/nginx
```

Установить Docker Desktop на Ваш компьютер и запустить его.

Создать директории infra файл .env и заполнить его своими данными:

```
SECRET_KEY=django_secret_key
ALLOWED_HOSTS=127.0.0.1 localhost
DEBUG=False

POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
DB_NAME=...
DB_HOST=...
DB_PORT=...

CELERY_BROKER_URL=...
CELERY_RESULT_BACKEND=...
```
В env.example есть все данные.

Запустить оркестр контейнеров:

```
docker compose up
```

Дождаться сборки и запуска всех контейнеров и в другом окне терминала выполнить миграции:

```
docker compose exec backend python manage.py migrate 
```

Собрать и скопировать статику Django:

```
docker compose exec backend python manage.py collectstatic
```
```
docker compose exec backend cp -r /app/static/. /backend_static/static/ 
```

Запустить тесты:

```
docker compose exec backend pytest
```

### Автор:

Михаил Алексенцев

[![Telegram](https://img.shields.io/badge/aleksentcev-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&link=https://t.me/aleksentcev)](https://t.me/aleksentcev)
