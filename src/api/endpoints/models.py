from pydantic import BaseModel


class Move(BaseModel):
    origin: int
    target: int
