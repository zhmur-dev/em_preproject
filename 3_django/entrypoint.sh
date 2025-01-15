#!/bin/bash

set -e

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic

# Copy static files
echo "Copying static files..."
cp -r static/. /static/

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.ru', 'admin')" | python manage.py shell

# Start Gunicorn
echo "Staring Gunicorn..."
exec "$@"