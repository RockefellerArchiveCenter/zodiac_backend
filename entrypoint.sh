#!/bin/bash

# Copy config file if it doesn't exist
if [ ! -f aurora/config.py ]; then
    echo "Copying example config file"
    cp zodiac_backend/config.py.example zodiac_backend/config.py
fi

# Apply database migrations
echo "Apply database migrations"
./wait-for-it.sh db:5432 -- python manage.py migrate

#Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:${APPLICATION_PORT}
