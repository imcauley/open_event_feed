import xml.etree.ElementTree as ET

from open_event_feed.event_item import EventItem


class FormattingError(Exception):
    pass


def event_items_from_xcal(xcal_filepath):
    xml_root = ET.parse(xcal_filepath).getroot()
    return event_items_from_xcal_tree(xml_root)


def event_items_from_xcal_string(xcal):
    xml_root = ET.fromstring(xcal)
    return event_items_from_xcal_tree(xml_root)


def event_items_from_xcal_tree(xcal_tree):
    if xcal_tree.tag != "iCalendar":
        raise FormattingError

    calendar = None
    for child in xcal_tree:
        if child.tag == "vcalendar":
            calendar = child

    if calendar is None:
        raise FormattingError

    for item in calendar:
        if item.tag == "vevent":
            event_item = vevent_to_event_item(item)
            yield event_item


def vevent_to_event_item(vevent):
    attributes_map = {
        "summary": "title",
        "url": "link",
        "description": "description",
        "dtstart": "start_datetime",
        "dtend": "end_datetime",
        "location": "location",
        "categories": "categories",
    }

    attributes = {}

    for attribute in attributes_map.keys():
        found_attribute = vevent.find(attribute)
        if found_attribute is not None:
            attributes[attributes_map[attribute]] = found_attribute.text

    return EventItem(**attributes)
