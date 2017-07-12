import xml.sax as sax
import re

from core.module import Module
from core.line_listener import LineListener

class RoomHandler(sax.ContentHandler):

    def __init__(self):
        self.CurrentData = ""
        self.data = {}

    def startElement(self, tag, attributes):
        if tag != "room":
            return

        title = attributes["title"]
        vnum = attributes["id"]

        if title in self.data:
            self.data[title].append(vnum)
        else:
            self.data[title] = [vnum]

    def get_data(self):
        return self.data
    

class MapModule(Module, LineListener):

    def __init__(self, *args):
        super(MapModule, self).__init__(*args)
        self.rooms = {}
        self.__load_map_data()

        self.triggers = [
                re.compile("^You divine the location of this death as (.+) in +\.$"),
                re.compile("^You pick up the faint scent of \w+ at (.+) in .+\.$"),
                re.compile("^You see that \w+ is at (.+) in .+\.$"),
                ]

    def __load_map_data(self):
        handler = RoomHandler()
        print(" - Parsing map")
        sax.parse("/home/linus/muds/aetolia/map.xml", handler)
        self.rooms = handler.get_data()

    def parse_line(self, line):
        for reg in self.triggers:
            match = reg.match(line)
            if match and match.group(1) in self.rooms:
                print("Room(s): %s" % ", ".join(self.rooms[match.group(1)]))
