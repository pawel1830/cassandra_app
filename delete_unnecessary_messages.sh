#!/bin/sh
echo "Remove messages older than 5 mins"
python /app/manage.py delete_unnecessary_messages