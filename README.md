### Запуск приложения:
```docker-compose up```

#### Для локального запуска в папке с проектом должен лежать .env файл с переменными, указанными ниже.
Пример содержимого .env:
```
RABBIT_HOST=localhost
RABBIT_PORT=5672
RABBIT_USER=rq
RABBIT_PASSWORD=rq
QUEUE_NAME=line_provider
INTERVAL_TO_SLEEP_SEC=1
```