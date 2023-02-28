#!/usr/bin/env bash
# exit on error
set -o errexit
pip install --upgrade pip

pip install django
pip install django-environ


python manage.py collectstatic --no-input
python manage.py migrate