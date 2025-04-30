#!/bin/bash
set -e


# Wait for postgres to accept connections
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Migrations are being made..."
python manage.py makemigrations common users

echo "Running Django migrations..."
python manage.py migrate --no-input
python manage.py migrate django_celery_beat --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 core.wsgi
