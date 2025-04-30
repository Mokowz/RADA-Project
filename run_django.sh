#!/bin/bash

# Wait for postgres to accept connections
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py makemigrations common core users

python manage.py migrate --no-input
python manage.py migrate django_celery_beat --no-input

python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 core.wsgi
