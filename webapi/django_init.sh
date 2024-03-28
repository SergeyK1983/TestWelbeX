#!/bin/sh

echo "=== Django start !!! ==="

echo "Django migrate ... "
python manage.py migrate

VAR=`tail -n 1 ./.env`

if [ "$VAR" = "GET_INIT=do_it" ]
then

    echo "Django collectstatic ... "
    python manage.py collectstatic --no-input

    echo "Django import uszips ... "
    python manage.py importuszips

    echo "Django import cargo ... "
    python manage.py importcargo

    echo "Django import cars ... "
    python manage.py importcars

    echo "Django init_admin ... "
    python manage.py initadmin

    python /backend/transport/management/get_change_env.py
    chmod 755 /backend/.env

fi

echo "Run ... "
gunicorn webapi.wsgi:application --bind 0.0.0.0:8000
