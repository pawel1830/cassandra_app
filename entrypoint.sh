#!/bin/sh
python /app/check_cassandra.py
ret=$?
if [ $ret -ne 0 ]; then
  echo "Cannot connect to Cassandra database"
  exit 1
fi
echo "Sync cassandra"
python manage.py sync_cassandra
exec "$@"