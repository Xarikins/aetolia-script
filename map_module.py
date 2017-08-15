import xml.sax as sax
import re
import urllib3 as urllib

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
    

class MapModule(Module):

    def __init__(self, *args):
        super(MapModule, self).__init__(*args)
        self.rooms = {}
        self.__load_map_data()

        callback_definition = {
                "fun": self.show_room,
                "arg": "'%P0' '%P1'",
                }

        self.state["gag_builder"].build({
            "^You divine the location of this death as (.+) in .+\.$": callback_definition,
            "^You pick up the faint scent of \w+ at (.+)\.$": callback_definition,
            "^You see that \w+ is at (.+) in .+\.$": callback_definition,
            "^You see \w+ at (.+)\.$": callback_definition,
            "^ \-  (.+)$": callback_definition,
            })

        self.state["alias_builder"].build({
            "mupdate": self.update_map,
            })
        self.state["alias_builder"].build({
            "^rf (.*)$": {
                "fun": self.room_find,
                "arg": "'%P1'",
                },
            }, "regexp")

    def update_map(self):
        http = urllib.PoolManager()
        print("Downloading map...")
        response = http.request("GET", self.state["settings"]["map_url"])
        with open(self.state["settings"]["map_file"], "w") as file:
            file.write(str(response.data, "utf-8"))
        print("...DONE")
        self.__load_map_data()

    def __load_map_data(self):
        handler = RoomHandler()
        print(" - Parsing map")
        sax.parse(self.state["settings"]["map_file"], handler)
        self.rooms = handler.get_data()

    def room_find(self, room):
        self.show_room(room, room)

    def show_room(self, line, room):
        if room in self.rooms:
            result = self.rooms[room]
            if len(result) > 1:
                self.mud.echop("%s ( Room(s): @{Cred}%s@{n} )" % (line, ", ".join(result)))
            else:
                self.mud.echop("%s ( Room: @{Cred}%s@{n} )" % (line, ", ".join(result)))
        else:
            self.mud.echop("%s ( Room: @{Cred}none@{n} )" % line)
