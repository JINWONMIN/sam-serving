from pydantic import BaseModel
from typing import List


class ClickList(BaseModel):
    points: List[int]
    labels: List[int]
    session_id: str


class Rectangle(BaseModel):
    startX: int
    startY: int
    endX: int
    endY: int
    session_id: str


class Add(BaseModel):
    session_id: str


class ImageRequests(BaseModel):
    image: str
    session_id: str