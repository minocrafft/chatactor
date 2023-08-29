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
    summary: Optional[str] = None
    speaking_style: Optional[str] = None
    birth: Optional[str] = None
    death: Optional[str] = None
    events: Optional[List[Event]] = None
