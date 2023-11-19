from fastapi import FastAPI, Query
import elasticsearch
from elasticsearch_util import check_connection, create_index, set_subtitles_mapping
from datetime import datetime
from starlette.responses import JSONResponse

app = FastAPI()

esclient = elasticsearch.Elasticsearch(
    ["http://elasticsearch:9200"],
    maxsize=10,
    timeout=30,
)


@app.get("/")
def filter_logs(
    level: str = None,
    message: str = None,
    resourceId: str = None,
    timestamp_start: datetime = None,
    timestamp_end: datetime = None,
    traceId: str = None,
    spanId: str = None,
    commit: str = None,
    parentResourceId: str = None,
    regex_fields: str = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    query = {
        "bool": {
            "must": [],
        }
    }

    if level:
        query["bool"]["must"].append({"term": {"level": level}})

    if message:
        if "message" in regex_fields:
            query["bool"]["must"].append(
                {
                    "regexp": {
                        "message": {
                            "value": message,
                            "flags": "ALL",
                            "case_insensitive": True,
                            "rewrite": "constant_score",
                        }
                    }
                }
            )
        else:
            query["bool"]["must"].append({"match": {"message": message}})

    if resourceId:
        query["bool"]["must"].append({"term": {"resourceId": resourceId}})

    if timestamp_start and timestamp_end:
        query["bool"]["must"].append(
            {
                "range": {
                    "timestamp": {
                        "gte": timestamp_start.isoformat(),
                        "lte": timestamp_end.isoformat(),
                    }
                }
            }
        )

    if traceId:
        query["bool"]["must"].append({"term": {"traceId": traceId}})

    if spanId:
        query["bool"]["must"].append({"term": {"spanId": spanId}})

    if commit:
        query["bool"]["must"].append({"term": {"commit": commit}})

    if parentResourceId:
        query["bool"]["must"].append({"term": {"parentResourceId": parentResourceId}})

    try:
        result = esclient.search(
            index="logs",
            body={"query": query, "from": (page - 1) * size, "size": size},
        )

        response = {
            "total": result["hits"]["total"]["value"],
            "page": page,
            "size": size,
            "pages": (result["hits"]["total"]["value"] // size) + 1,
            "logs": [hit["_source"] for hit in result["hits"]["hits"]],
        }

        return JSONResponse(content=response, status_code=200)

    except elasticsearch.ElasticsearchException as e:
        print(e)

        return JSONResponse(
            content={"message": "An error occurred while filtering the logs"},
            status_code=500,
        )


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    check_connection()
    create_index("logs")
    set_subtitles_mapping()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    esclient.transport.close()
