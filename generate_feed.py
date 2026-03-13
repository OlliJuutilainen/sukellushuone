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

rss = ET.Element("rss", version="2
