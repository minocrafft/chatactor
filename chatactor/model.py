from typing import Optional, List
from pydantic import BaseModel


class Event(BaseModel):
    event_name: str
    event_date: str
    event_description: str


class Actor(BaseModel):
    name: str
    image: Optional[str] = None
    occupation: Optional[str] = None
    birth: Optional[str] = None
    death: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None  # markdown


class CardModel(BaseModel):
    name: str
    image: str
    imagedata: str
