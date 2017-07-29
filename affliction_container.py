import json
import re

class AfflictionContainer():

    def __init__(self):
        self.afflictions = {}
        self.active_afflictions = {}
        self.pill_afflictions = {}
        self.poultice_afflictions = {}
        self.smoke_afflictions = {}
        self.writhe_afflictions = {}
        self.__load_afflictions()

        self.afflict_trigger = re.compile("^You are afflicted with (.+)\.$")
        self.discover_trigger = re.compile("^You have discovered (.+)\.$")
        self.cure_trigger = re.compile("^You have cured (.+)\.$")


    def __load_afflictions(self):
        affs = []
        with open("/home/linus/muds/aetolia/afflictions.json") as file:
            affs = json.loads(file.read())

        for aff in affs:
            self.afflictions[aff["name"]] = aff

    def __activate(self, name):
        if name not in self.afflictions:
            return False

        aff = self.afflictions[name]
        self.active_afflictions[name] = aff
        if aff["smoke"]:
            self.smoke_afflictions[name] = aff
        if aff["pill"]:
            self.pill_afflictions[name] = aff
        if aff["poultice"]:
            self.poultice_afflictions[name] = aff
        if aff["special"] == "writhe":
            self.writhe_afflictions[name] = aff

        return True

    def __deactivate(self, name):
        if name not in self.active_afflictions:
            return False

        aff = self.active_afflictions[name]
        del self.active_afflictions[name]
        if aff["smoke"]:
            del self.smoke_afflictions[name]
        if aff["pill"]:
            del self.pill_afflictions[name]
        if aff["poultice"]:
            del self.poultice_afflictions[name]
        if aff["special"] == "writhe":
            del self.writhe_afflictions[name]

        return True

    def parse_line(self, line):
        match = self.afflict_trigger.match(line)
        if (match):
            self.__activate(match.group(1))
            return
        match = self.discover_trigger.match(line)
        if (match):
            self.__activate(match.group(1))
            return
        match = self.cure_trigger.match(line)
        if (match):
            self.__deactivate(match.group(1))
            return

    def get_active(self):
        return self.active_afflictions

    def get_smoke(self):
        return self.smoke_afflictions

    def get_pill(self):
        return self.pill_afflictions

    def get_poultice(self):
        return self.poultice_afflictions

    def get_writhe(self):
        return self.writhe_afflictions
