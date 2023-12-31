#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py showmigrations -l

gunicorn  service.wsgi:application --bind 0.0.0.0:8000

exec "$@"