import os
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from schemas.logs import Log

app = FastAPI()

producer = AIOKafkaProducer(
    bootstrap_servers=f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}",
    client_id="my-producer",
)


@app.post("/")
async def produce_message(log: Log):
    try:
        print("PRODUCER", log.model_dump_json().encode("utf-8"))
        await producer.send_and_wait("logs", log.model_dump_json().encode("utf-8"))

        return {"message": "Message sent"}
    except Exception as e:
        print("error occurred: ", e)
        return {"message": "Message not sent"}


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await producer.stop()
