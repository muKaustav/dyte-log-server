import os
import httpx
from datetime import datetime
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from schemas.logs import Log

logs = APIRouter()


async def send_post_request(url, data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        return response


async def send_get_request(url, query_params):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=query_params)
        return response


@logs.get("/")
async def get_log(
    level: str = Query(None, min_length=1, max_length=10),
    message: str = Query(None, min_length=1, max_length=100),
    resourceId: str = Query(None, min_length=1, max_length=100),
    timestamp_start: datetime = Query(datetime(1970, 1, 1)),
    timestamp_end: datetime = Query(datetime.now()),
    traceId: str = Query(None, min_length=1, max_length=100),
    spanId: str = Query(None, min_length=1, max_length=100),
    commit: str = Query(None, min_length=1, max_length=100),
    parentResourceId: str = Query(None, min_length=1, max_length=100),
    regex_fields: str = Query(None, min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """
    Check connection to Elasticsearch
    """
    try:
        query_params = {
            "level": level,
            "message": message,
            "resourceId": resourceId,
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
            "traceId": traceId,
            "spanId": spanId,
            "commit": commit,
            "parentResourceId": parentResourceId,
            "regex_fields": regex_fields,
            "page": page,
            "size": size,
        }

        response = await send_get_request(os.getenv("ELASTICSEARCH_URL"), query_params)

        return JSONResponse(status_code=200, content=response.json())

    except Exception as e:
        response = {
            "data": {
                "message": "Something went wrong: " + str(e),
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            },
        }

        return JSONResponse(status_code=500, content=response)


@logs.post("/")
async def add_log(log: Log):
    """
    Receive logs from the client and send them to Kafka
    """
    try:
        await send_post_request(os.getenv("KAFKA_URL"), data=log.model_dump_json())

        message = {
            "data": {
                "message": "Message sent",
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            },
        }

        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        message = {
            "data": {
                "message": "Something went wrong: " + str(e),
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            },
        }

        return JSONResponse(status_code=500, content=message)
