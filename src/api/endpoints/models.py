from pydantic import BaseModel


class Move(BaseModel):
    target: int
    origin: int


class MoveScore(BaseModel):
    move: Move
    score: int


class CheckersPiece(BaseModel):
    position: int
    player: int
    king: bool
