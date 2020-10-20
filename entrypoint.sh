#!/bin/sh
echo "Sync cassandra"
python manage.py sync_cassandra
exec "$@"