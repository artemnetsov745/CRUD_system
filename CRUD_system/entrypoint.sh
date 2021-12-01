#! /bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py loaddata group_init.json
python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --no-input

exec gunicorn djangoapp.wsgi:application - b 0.0.0.0:8000 --reload