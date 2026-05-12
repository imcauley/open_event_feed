import datetime
import json
import xml.etree.ElementTree as ET

class EventItemJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, date)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)

def xcal_from_event_items(event_item_list, file):
    # From RFC https://www.rfc-editor.org/rfc/rfc6321.html

    root = ET.Element('icalendar')
    root.set('xmlns', 'urn:ietf:params:xml:ns:icalendar-2.0')

    calendar = ET.SubElement(root, 'vcalendar')
    components = ET.SubElement(calendar, 'components')

    for event_item in event_item_list:
        components.append(event_item.to_xcal_vevent())

    tree = ET.ElementTree(root)
    ET.indent(tree)

    tree.write(file, encoding="UTF-8", xml_declaration=True)

