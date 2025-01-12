#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

chmod -R 755 /app/static

gunicorn onaylf.wsgi:application --bind 0.0.0.0:8100 --timeout 120
