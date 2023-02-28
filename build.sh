#!/usr/bin/env bash
# exit on error
set -o errexit
pip install --upgrade pip

pip install django
pip install django-environ
pip install dj-database-url
pip install djangorestframework

python manage.py collectstatic --no-input
python manage.py migrate