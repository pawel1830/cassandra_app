from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from test_project.api.models import Message


class Command(BaseCommand):
    help = 'Remove messages older than 5 minutes'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        query = Message.objects.filter(created_at__gte=now-timedelta(minutes=5))
        message_uuids = [message['uuid'] for message in query]
        Message.objects.filter(uuid__in=message_uuids).delete()
