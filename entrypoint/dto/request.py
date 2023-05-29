from pydantic import BaseModel


class MustJump(BaseModel):
    distance: int
    velocity: int
    height: int
    posix: int