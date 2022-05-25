#!/bin/sh
python manage.py migrate
python manage.py createsuperuser --username ${DJANGO_SUPERUSER_USER} --email ${DJANGO_SUPERUSER_EMAIL} --noinput || true
python manage.py collectstatic --noinput
gunicorn $GUNICORN_ARGS



