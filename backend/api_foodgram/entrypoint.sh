#!/bin/bash

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
elif [ $1 = "migrate-import" ]
  then
      python manage.py migrate
      python manage.py import_ingredients
elif [ $1 = "migrate-import-collectstatic" ]
  then
      python manage.py migrate
      python manage.py import_ingredients
      python manage.py collectstatic --noinput
elif [ $1 = "run" ]
  then
    exec $(which gunicorn) api_foodgram.wsgi:application --bind=0:8000
    exit $?
elif [ $1 = "all" ]
  then
      python manage.py migrate
      python manage.py import_ingredients
      python manage.py collectstatic
    exec $(which gunicorn) api_foodgram:application --bind=0:8000
    exit $?
else
  echo "Invalid argument"
  exit 1
fi