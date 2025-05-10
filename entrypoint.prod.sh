#!/usr/bin/env bash

python manage.py collectstatic --noinput
gunicorn --bind  0.0.0.0:8000 --workers 3 --timeout 120 blog.wsgi:application