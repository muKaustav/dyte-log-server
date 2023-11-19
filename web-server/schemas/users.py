from pydantic import BaseModel


class User(BaseModel):
    """
    Log schema
    """

    username: str
    password: str
    email: str
    role: str
