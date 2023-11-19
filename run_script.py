from fastapi import FastAPI, Query
import time
import httpx
import asyncio
from datetime import datetime, timedelta
import random

app = FastAPI()


async def send_post_request(url, data):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        await client.post(url, json=data)
        end_time = time.time()

        return end_time - start_time


def generate_random_data():
    start_date = datetime(2023, 9, 15, 8, 0, 0)
    end_date = start_date + timedelta(days=random.randint(1, 30))
    random_timestamp = start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

    data = {
        "level": random.choice(["error", "info", "warning"]),
        "message": f"Message {random.randint(1, 100)}",
        "resourceId": f"server-{random.randint(1000, 9999)}",
        "timestamp": random_timestamp.isoformat() + "Z",
        "traceId": f"abc-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}",
        "spanId": f"span-{random.randint(100, 999)}",
        "commit": f"{random.randint(100000, 999999)}",
        "metadata": {"parentResourceId": f"server-{random.randint(1000, 9999)}"},
    }

    return data


@app.post("/")
async def root(iter: int = Query(..., gt=0)):
    URL = "http://127.0.0.1:3000/"


    tasks = [send_post_request(URL, generate_random_data()) for _ in range(iter)]
    response_times = await asyncio.gather(*tasks)

    average_response_time = sum(response_times) / len(response_times)

    return {"message": f"Average Response Time: {average_response_time:.4f} seconds"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run_script:app", host="127.0.0.1", port=5000, reload=True)
