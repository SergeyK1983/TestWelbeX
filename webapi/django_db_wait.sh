#!/bin/sh

echo "=== Django start wait postgres! ==="

if [ "$DATABASE" = "postgres" ]
then
    echo "=== Waiting ... ==="

    while ! nc -z $HOST $PORT; do
      sleep 5.0
    done

    echo "=== PostgreSQL started ==="
fi

# exec "$@"