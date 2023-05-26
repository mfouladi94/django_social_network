#!/bin/bash

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate

# Run Django runserver
gunicorn --bind 0.0.0.0:8000 django_social_network.wsgi