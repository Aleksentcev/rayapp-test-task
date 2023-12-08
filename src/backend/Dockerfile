FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["daphne", "--bind", "0.0.0.0", "--port", "8000", "test_task.asgi:application"]
