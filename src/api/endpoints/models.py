from typing import List

from pydantic import BaseModel


class Move(BaseModel):
    target: int
    origin: int


class CheckersPiece(BaseModel):
    position: int
    player: int
    king: bool

