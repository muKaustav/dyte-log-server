import os
import json
import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from app.cassandra_util import CassandraFactory
import elasticsearch

app = FastAPI()

consumer = AIOKafkaConsumer(
    bootstrap_servers=f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}",
    group_id="my-group",
    auto_offset_reset="earliest",
)

cassandra_obj = CassandraFactory()
session = cassandra_obj.get_session()

es_client = elasticsearch.Elasticsearch(
    [f"http://{os.getenv('ELASTIC_HOST')}:{os.getenv('ELASTIC_PORT')}"]
)


async def consume_and_insert_to_cassandra():
    consumer.subscribe(["logs"])

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            metadata = json.dumps(data["metadata"]).replace("'", "''")
            data["metadata"] = metadata

            cassandra_obj.insert_log(data)
            es_client.index(index="logs", body=data)

            print("Message consumed and inserted to Cassandra, Elasticsearch")

    except Exception as e:
        print("error occurred:", e)

    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await consumer.start()
    asyncio.create_task(consume_and_insert_to_cassandra())


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await consumer.stop()
