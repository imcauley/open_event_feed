from dataclasses import dataclass
from typing import Optional, List, Dict
import datetime
import json

class EventItemJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)

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

    additional_data: Optional[Dict] = None
    # validations
    # needs start_datetime if end_datetime exists
    # needs organizer_link if organizer name exists

    def toJSON(self):
        return json.dumps(
            self.__dict__,
            cls=EventItemJSONEncoder,
            sort_keys=True)

if __name__ == "__main__":
    e1 = EventItem(title="test", link="sdfklsdf", start_datetime=datetime.datetime.now(), additional_data={"test": "abc123"})
    print(e1.toJSON())