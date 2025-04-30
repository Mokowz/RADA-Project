#!/bin/bash
set -e

sleep 15
# echo "Waiting for database host ${POSTGRES_HOST}..."
# # First, wait for the database service itself to be reachable
# # Uses netcat (nc), requires 'netcat-openbsd' or similar package
# while ! nc -z "$POSTGRES_HOST" 5432; do
#   echo "Database unavailable - sleeping"
#   sleep 1
# done
# echo "Database available!"


# echo "Waiting for django_celery_beat migrations..."
# # Loop until the psql command succeeds (exit code 0), indicating the table exists
# # Requires 'postgresql-client' package
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\dt django_celery_beat_periodictask' > /dev/null 2>&1; do
#   >&2 echo "Migrations not applied yet (table django_celery_beat_periodictask not found) - sleeping"
#   sleep 1
# done

# >&2 echo "Migrations applied - executing command"
# # Execute the command passed as arguments to this script
# exec "$@"