from fastapi import FastAPI, Query
import time
import httpx
import asyncio

app = FastAPI()


async def send_post_request(url, data):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        await client.post(url, json=data)
        end_time = time.time()

        return end_time - start_time


@app.post("/")
async def root(iter: int = Query(..., gt=0)):
    URL = "http://127.0.0.1:3000/"

    data = {
        "level": "error",
        "message": "Failed to connect to DB",
        "resourceId": "server-1234",
        "timestamp": "2023-09-15T08:00:00Z",
        "traceId": "abc-xyz-123",
        "spanId": "span-456",
        "commit": "5e5342f",
        "metadata": {"parentResourceId": "server-0987"},
    }

    tasks = [send_post_request(URL, data) for _ in range(iter)]
    response_times = await asyncio.gather(*tasks)

    average_response_time = sum(response_times) / len(response_times)

    return {"message": f"Average Response Time: {average_response_time:.4f} seconds"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run_script:app", host="127.0.0.1", port=5000, reload=True)
