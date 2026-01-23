from dataclasses import dataclass
from typing import Optional, List
import datetime

@dataclass
class EventItem:
    title: str
    link: str

    description: Optional[str] = None
    language: Optional[str] = None
    categories: Optional[List[str]] = None
    organizer_link: Optional[str] = None
    organizer_name: Optional[str] = None

    start_datetime: Optional[datetime.datetime] = None
    end_datetime: Optional[datetime.datetime] = None

    location: Optional[str] = None
    # validations
    # needs start_datetime if end_datetime exists
    # needs organizer_link if organizer name exists

if __name__ == "__main__":
    e1 = EventItem(title="test", link="sdfklsdf")
