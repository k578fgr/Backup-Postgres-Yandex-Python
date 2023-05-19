#!/usr/bin/python3

import psycopg2
import os
import datetime
import boto3


TIME_ZONE = 'Europe/Moscow'
DB_NAME = <name>
DB_USER = <db_name>
DB_PASS = <passwod>
DB_HOST = <host>
DB_PORT = <port>
DB_FILE = '/tmp/backup_db.sql.gz'


# Подключение к БД
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    host=DB_HOST,
    port=DB_PORT
)

# Создание курсора
cur = conn.cursor()

# Получение текущей даты и времени для имени файла
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Имя файла
filename = "backup_{}.sql".format(now)

# Выполнение команды для создания дампа БД

command = f"pg_dump -h localhost -U {DB_USER} -p {DB_PORT} -F c -f {filename} {DB_NAME}"
os.system(command)

# Инициализация клиента для работы с Yandex Object Storage
s3 = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net/имя_бакета',
    aws_access_key_id='key_id',
    aws_secret_access_key='secret_key'
)

# Загрузка файла в Yandex Object Storage
file = open(f"./{filename}", "rb")
s3.upload_fileobj(file, "Папка_внутри_бакета", filename)

# Удаление файла
os.remove(filename)

# Закрытие курсора и соединения с БД
cur.close()
conn.close()
