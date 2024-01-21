#!/bin/sh

gunicorn onaylf.wsgi:application --bind 0.0.0.0:8000
