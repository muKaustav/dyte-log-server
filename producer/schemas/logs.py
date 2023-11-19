from pydantic import BaseModel


class Log(BaseModel):
    """
    Log schema
    """

    level: str
    message: str
    resourceId: str
    timestamp: str
    traceId: str
    spanId: str
    commit: str
    metadata: dict
