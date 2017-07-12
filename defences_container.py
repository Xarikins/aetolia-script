import json
import re

class DefencesContainer():

    def __init__(self, state):
        self.state = state
        self.defences = {}
        self.combat_defences = {}
        self.missing_defences = {}
        self.__load_defences()
        self.gain_trigger = re.compile("^You have gained the (.+) defence\.$")
        self.lose_trigger = re.compile("^Your (.+) defence has been stripped\.$")
        self.defence_trigger = re.compile("^You have the following active defences\:$")

    def __load_defences(self):
        defs = []
        with open("/home/linus/muds/aetolia/defences.json") as file:
            defs = json.loads(file.read())

        for defence in defs:
            if defence["combat_defence"]:
                self.combat_defences[defence["name"]] = defence
            else:
                self.defences[defence["name"]] = defence

    def __activate(self, name):
        fight_mode = self.state["mode"]["fight"]

        if name in self.defences:
            self.missing_defences[name] = self.defences[name]
        elif fight_mode and name in self.combat_defences:
            self.missing_defences[name] = self.combat_defences[name]

    def __deactivate(self, name):
        if not name in self.missing_defences:
            return
        del self.missing_defences[name]

    def __activate_all(self):
        if self.state["mode"]["fight"]:
            self.missing_defences = dict(self.defences, **self.combat_defences)
        else:
            self.missing_defences = dict(self.defences)

    def parse_line(self, line):
        match = self.gain_trigger.match(line)
        if match:
            self.__deactivate(match.group(1))
        match = self.lose_trigger.match(line)
        if match:
            self.__activate(match.group(1))
        match = self.defence_trigger.match(line)
        if match:
            self.__activate_all()

        tmp_missing = list(self.missing_defences.values())
        for defence in tmp_missing:
            if defence["defence_line"] == line:
                self.__deactivate(defence["name"])

    def get_missing(self):
        return self.missing_defences.values()
