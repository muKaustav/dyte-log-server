from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    """
    Message schema
    """

    id: int
    message: str
    created_at: str
