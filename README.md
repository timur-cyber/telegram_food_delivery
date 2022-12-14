# Telegram бот для заказа доставки на Django

## Установка Python окружения

1. Скачать на ПК интерпретатор языка Python (версии 3.7 или новее).
2. Желательно поставить виртаульное окружение в директории проекта:
    * `python3 -m venv name`
3. Следом, надо активировать окружение:
    * Windows `.\env\Scripts\activate`
    * Linux/MacOS `source env/bin/activate`
4. Установить необходимые библиотеки с помощью команды:
    * `python -m pip install -r requirements.txt`

## Настройка ключей

### БД Postgres

Для настройки БД надо перейти в директорию **./.envs/.postgres/**, создать файл **.postgres** и по примеру файла *
*.postgres.example** заполнить файл окружения БД Postgres.

Подробная информация по созданию БД с помощью
PostgreSQL: https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e

### Окружение Django

Настройка окружения Django производится через **./djangoXtelegram/**, путём создания файла окружения  **.env** по
примеру файла **.env.example**

Для получения **TOKEN** необходимо создать Telegram бота и получить токен через BotFather.

Подробнее: https://core.telegram.org/bots

Для получения **SECRET** необходимо создать Django проект и получить секретный ключ.

Подробнее: https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key

Для получения **NGROK_AUTH_TOKEN** необходимо зарегистриовать аккаунт в ngrok.com и получить токен.

Подробнее: https://ngrok.com/docs/

## Запуск бота

### Docker

Для запуска бота рекомендуется использовать Docker. 

Подробнее: https://docs.docker.com/

Чтобы запустить проект, в терминале нужно ввести команду:
```commandline
docker-compose up
```
Чтобы запустить проект в фоновом режиме, в терминале нужно ввести команду:
```commandline
docker-compose up -d
```

### Terminal
Для запуска бота нативно через интепретатор Python необходимо ввести данные команды:
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json
python manage.py runserver 0.0.0.0:8000
```
Перед запуском нативно через терминал нужно убедиться что СУБД Postgres работает на локальной машине и что на ней установлены необходимые настройки БД.
