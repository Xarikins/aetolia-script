import re
import json

from collections import deque

from core.module import Module
from core.line_listener import LineListener
from core.prompt_listener import PromptListener

class AfflictionParser(Module, LineListener, PromptListener):

    def __init__(self, *args):
        super(AfflictionParser, self).__init__(*args)
        self.enabled = False
        self.current_affliction = ""
        self.triggers = {
                "name": "^Affliction\:\s+(\w+.+)\.$",
                "diagnose": "^Diagnose\:\s+(\w+.+\.)$",
                "cure_message": "^Cure message\:\s+(\w+.+\.)$",
                "cure_message_obs": "^Cure message 3p\:\s+(\w+.+\.)$",
                "body_part": "^Body part\:\s+(\w+.+\.)$",
                "type": "^Type:\s+\[(.)\]Physical\s+\[(.)\]Mental\s+\[(.)\]Venom$",
                "pill": "^Pill\:\s+(\w+.+)\.$",
                "poultice": "^Poultice\:\s+(\w+.+)\.$",
                "smoke": "^Smoked\:\s+(\w+.+)\.$",
                "special": "^Special\:\s+(\w+.+)\.$",
                }
        self.ctriggers = {}
        for desc, regex in self.triggers.items():
            self.ctriggers[desc] = re.compile(regex)

        self.data = self.__new_data()
        self.all_data = []

        aliases = {
                "afflict_grab": self.toggle_affliction_grabbing,
                "save_affs": self.save_afflictions,
                }

        self.state["alias_builder"].build(aliases)
        self.afflictions = deque([])

    def __store(self, data):
        print("Storing: %s" % data["name"])
        self.all_data.append(data)
        self.data = self.__new_data()

    def __new_data(self):
        return {
                "name": "",
                "diagnose": "",
                "cure_message": "",
                "cure_message_obs": "",
                "body_part": "",
                "type": { 
                    "physical": False,
                    "mental": False,
                    "venom": False,
                    },
                "pill": "",
                "poultice": "",
                "smoke": "",
                "special": "",
                "priority": 0,
                }

    def toggle_affliction_grabbing(self):
        self.enabled = not self.enabled
        if self.enabled:
            print("Grabbing enabled")
            self.__load_afflictions()
        else:
            print("Grabbing disabled")
            self.afflictions.clear()

    def __load_afflictions(self):
        print("Reading afflictions from file")
        with open("/home/linus/muds/aetolia/afflictions.list", "r") as f:
            for aff in f:
                self.afflictions.append(aff.strip())
        print("Done")
        print("Starting...")
        self.__request_affliction()

    def __request_affliction(self):
        if len(self.afflictions):
            self.state["communicator"].send("afflict %s show" % self.afflictions.popleft())
        else:
            self.enabled = False
            print("DONE")
        print("%d read, %d remaining" % (len(self.all_data), len(self.afflictions)))

    def save_afflictions(self):
        print("Writing afflictions to file")
        with open("afflictions.json", "w") as f:
            f.write(json.dumps(self.all_data, indent=4, separators=(",",": ")))

    def parse_prompt(self, line):
        if self.enabled and line.startswith("H:"):
            self.__request_affliction()

    def parse_line(self, line):
        if not self.enabled:
            return

        for name, reg in self.ctriggers.items():
            match = reg.match(line)

            if not match:
                continue

            if name == "type":
                self.data["type"]["physical"] = match.group(1) == "x"
                self.data["type"]["mental"] = match.group(2) == "x"
                self.data["type"]["venom"] = match.group(3) == "x"
            else:
                if match.group(1) != "Nothing":
                    result = match.group(1)
                    if name != "cure_message" and name != "cure_message_obs":
                        result = result.lower()
                    self.data[name] = result
                else:
                    self.data[name] = ""
            
            #print("Matched: %s -> %s" % (name, match.group(1).lower()))
            if name == "special":
                self.__store(self.data)

