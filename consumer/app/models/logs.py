import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class LogModel(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    level = columns.Text(required=True)
    message = columns.Text(required=True)
    resourceId = columns.Text(required=True)
    timestamp = columns.DateTime(required=True)
    traceId = columns.Text(required=True)
    spanId = columns.Text(required=True)
    commit = columns.Text(required=True)
    metadata = columns.Map(columns.Text, columns.Text)
