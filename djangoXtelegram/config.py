from decouple import config

# Telegram
TOKEN = config('TOKEN')

# Django
SECRET = config('SECRET')
REGION = config('REGION')

# Postgres
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PWD = config('DB_PWD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
