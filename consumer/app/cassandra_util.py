import os
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime


class CassandraFactory:
    def __init__(self):
        self.KEYSPACE = "dyte"
        self.HOSTS = ["cassandra"]
        self.AUTH_PROVIDER = PlainTextAuthProvider(
            username="cassandra", password="cassandra"
        )

        self.cluster = Cluster(
            contact_points=self.HOSTS,
            auth_provider=self.AUTH_PROVIDER,
            port=os.getenv("CASSANDRA_PORT"),
            protocol_version=4,
        )

        self.session = self.cluster.connect()
        self.session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {self.KEYSPACE} WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }}"
        )
        self.session.set_keyspace(self.KEYSPACE)

        self.session.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.KEYSPACE}.logs (
                id uuid PRIMARY KEY,
                level text,
                message text,
                resourceId text,
                event_timestamp timestamp,
                traceId text,
                spanId text,
                commit text,
                metadata text
            );
            """
        )

    def get_session(self):
        return self.session

    def insert_log(self, log):
        print("CASSANDRA", log)
        self.session.execute(
            f"""
            INSERT INTO {self.KEYSPACE}.logs (
                id,
                level,
                message,
                resourceId,
                event_timestamp,
                traceId,
                spanId,
                commit,
                metadata
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """,
            (
                uuid.uuid4(),
                log["level"],
                log["message"],
                log["resourceId"],
                datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                ),
                log["traceId"],
                log["spanId"],
                log["commit"],
                log["metadata"],
            ),
        )
