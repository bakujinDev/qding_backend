#!/usr/bin/env bash
# exit on error
set -o errexit
pip install --upgrade pip

poetry lock
poetry install
# pip install django
# pip install django-environ
# pip install dj-database-url
# pip install djangorestframework
# pip install djangorestframework-simplejwt

python manage.py collectstatic --no-input
python manage.py migrate