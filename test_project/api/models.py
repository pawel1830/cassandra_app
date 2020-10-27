import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class Message(DjangoCassandraModel):
    uuid = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Text(index=True)
    magic_number = columns.Integer(index=True)
    title = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.now())
    content = columns.Text(required=True)

    __options__ = {
        "default_time_to_live": 600
    }
