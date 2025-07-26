#!/bin/sh

echo "📦 Ожидаем PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "🔧 Выполняем миграции..."
python manage.py migrate

echo "🚀 Запускаем сервер..."
python manage.py runserver 0.0.0.0:8000
