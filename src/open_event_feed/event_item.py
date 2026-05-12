from dataclasses import dataclass
from typing import Optional, List, Dict
import datetime
import json
import xml.etree.ElementTree as ET

class EventItemJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EventItem):
            return {k:v for k,v in obj.__dict__.items() if v is not None}

        if isinstance(obj, (datetime.datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)

@dataclass
class EventItem:
    title: str
    link: str
    
    uid: Optional[str] = None

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

    def __post_init__(self):
        if type(self.start_datetime) == str:
            self.start_datetime = datetime.datetime.fromisoformat(self.start_datetime)
        if type(self.end_datetime) == str:
            self.start_datetime = datetime.datetime.fromisoformat(self.start_datetime)
        if self.uid is None:
            self.uid = f"{self.title}-{self.link}-{self.start_datetime.isoformat()}"

    def toJSON(self):
        return json.dumps(
            self,
            cls=EventItemJSONEncoder,
            sort_keys=True)

    @staticmethod
    def fromJSON(json_string):
        d = json.loads(json_string)
        return EventItem(**d)

    def to_xcal_vevent(self, tzid: str = "UTC") -> str:
        """
        Convert the event into xCal-style XML.
        """

        def isoformat(dt: datetime.datetime) -> str:
            if dt.tzinfo is not None:
                return dt.isoformat()
            return dt.isoformat()

        vevent = ET.Element("vevent")
        properties = ET.SubElement(vevent, "properties")

        # dtstamp
        dtstamp = ET.SubElement(properties, "dtstamp")
        dtstamp_dt = ET.SubElement(dtstamp, "date-time")
        dtstamp_dt.text = (
            datetime.datetime.utcnow()
            .replace(microsecond=0)
            .isoformat() + "Z"
        )

        # dtstart
        if self.start_datetime:
            dtstart = ET.SubElement(properties, "dtstart")

            params = ET.SubElement(dtstart, "parameters")
            tzid_el = ET.SubElement(params, "tzid")
            tzid_text = ET.SubElement(tzid_el, "text")
            tzid_text.text = tzid

            start_dt = ET.SubElement(dtstart, "date-time")
            start_dt.text = isoformat(self.start_datetime)

        # dtend
        if self.end_datetime:
            dtend = ET.SubElement(properties, "dtend")

            params = ET.SubElement(dtend, "parameters")
            tzid_el = ET.SubElement(params, "tzid")
            tzid_text = ET.SubElement(tzid_el, "text")
            tzid_text.text = tzid

            end_dt = ET.SubElement(dtend, "date-time")
            end_dt.text = isoformat(self.end_datetime)

        # summary
        summary = ET.SubElement(properties, "summary")
        summary_text = ET.SubElement(summary, "text")
        summary_text.text = self.title

        # description
        if self.description:
            description = ET.SubElement(properties, "description")
            description_text = ET.SubElement(description, "text")
            description_text.text = self.description

        # location
        if self.location:
            location = ET.SubElement(properties, "location")
            location_text = ET.SubElement(location, "text")
            location_text.text = self.location

        # url
        url = ET.SubElement(properties, "url")
        uri = ET.SubElement(url, "uri")
        uri.text = self.link

        # organizer
        if self.organizer_name or self.organizer_link:
            organizer = ET.SubElement(properties, "organizer")

            if self.organizer_link:
                organizer_uri = ET.SubElement(organizer, "cal-address")
                organizer_uri.text = self.organizer_link

            if self.organizer_name:
                params = ET.SubElement(organizer, "parameters")
                cn = ET.SubElement(params, "cn")
                cn_text = ET.SubElement(cn, "text")
                cn_text.text = self.organizer_name

        # categories
        if self.categories:
            categories = ET.SubElement(properties, "categories")
            for cat in self.categories:
                text = ET.SubElement(categories, "text")
                text.text = cat

        # language
        if self.language:
            lang = ET.SubElement(properties, "language")
            text = ET.SubElement(lang, "text")
            text.text = self.language

        # uid
        uid = ET.SubElement(properties, "uid")
        uid_text = ET.SubElement(uid, "text")
        uid_text.text = str(self.uid)

        return vevent

if __name__ == "__main__":
    e1 = EventItem(title="test", link="sdfklsdf", start_datetime=datetime.datetime.now(), additional_data={"test": "abc123"})
    print(e1)
    print(e1.toJSON())
    e2 = """
    {"additional_data": {"test": "abc123"}, "categories": null, "description": null, "end_datetime": null, "language": null, "link": "sdfklsdf", "location": null, "organizer_link": null, "organizer_name": null, "start_datetime": "2026-04-03T23:53:00.087549", "title": "test"}
    """
    print(EventItem.fromJSON(e2))
    xcal = e1.to_xcal_vevent()
    print(ET.dump(xcal))