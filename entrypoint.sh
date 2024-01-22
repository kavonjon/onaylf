#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

chmod -R 755 /static

gunicorn onaylf.wsgi:application --bind 0.0.0.0:8000
