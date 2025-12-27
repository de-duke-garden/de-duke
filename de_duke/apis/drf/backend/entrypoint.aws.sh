#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
# Ensure PORT is set in the environment or default to 8000
# This allows the server to run on the specified port
# exec uvicorn main.asgi:application --host 0.0.0.0 --port 8000
exec gunicorn --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main.asgi:application