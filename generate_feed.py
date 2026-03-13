from email.utils import formatdate
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

# Lue vanhat päivämäärät feed.xml:stä jos se on olemassa
old_dates = {}
if os.path.exists("feed.xml"):
    try:
        old_tree = ET.parse("feed.xml")
        for old_item in old_tree.findall(".//item"):
            guid = old_item.findtext("guid")
            pubdate = old_item.findtext("pubDate")
            if guid and pubdate:
                old_dates[guid] = pubdate
    except:
        pass

items = []
with open("jaksot.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("@", 1)
        if len(parts) == 2:
            items.append((parts[0].strip(), parts[1].strip()))

rss = ET.Element("rss", version="2.0")
rss.set("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "deep divinations, Deepdivenation"
ET.SubElement(channel, "link").text = "https://www.dropbox.com"
ET.SubElement(channel, "description").text = "Deep divinations inside a deepdive Nation"
ET.SubElement(channel, "language").text = "en"

for title, url in items:
    ext = url.split("?")[0].split(".")[-1].lower()
    mime = "audio/mpeg"
    url = url.replace("dl=0", "dl=1")
    guid = title.strip().lower().replace(" ", "-")
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "pubDate").text = old_dates.get(guid, formatdate())
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = title
    enc = ET.SubElement(item, "enclosure")
    enc.set("url", url)
    enc.set("length", "0")
    enc.set("type", mime)
    ET.SubElement(item, "guid").text = guid

xml_str = minidom.parseString(ET.tostring(rss, encoding="unicode")).toprettyxml(indent="  ")
xml_str = "\n".join(xml_str.split("\n")[1:])
with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)
print("feed.xml generoitu.")
