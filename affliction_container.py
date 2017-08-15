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
        self.focus_afflictions = {}
        self.__load_afflictions()
        self.predictions = set([])

        self.group_triggers = [
                (re.compile("^You are afflicted with (.+)\.$"), self.activate),
                (re.compile("^You have discovered (.+)\.$"), self.activate),
                (re.compile("^You have cured (.+)\.$"), self.deactivate),
                ]
        self.triggers = [
                (re.compile("^You are\:$"), self.clear_all_affs),
                ]
        self.predict_triggers = [
                (re.compile("^The Sun tarot is shadowed by the sickly glow of the Eclipse\.$"), [
                    "paresis",
                    "asthma"
                    ]),
                (re.compile("^The Moon tarot is shadowed by the sickly glow of the Eclipse\.$"), [
                    "stupidity",
                    "anorexia"
                    ]),
                ]


    def __load_afflictions(self):
        affs = []
        with open("/home/linus/muds/aetolia/afflictions.json") as file:
            affs = json.loads(file.read())

        for aff in affs:
            self.afflictions[aff["name"]] = aff

    def activate(self, name):
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
        if aff["type"]["mental"]:
            self.focus_afflictions[name] = aff

        self.unpredict(aff["name"])

        return True

    def deactivate(self, name):
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
        if aff["type"]["mental"]:
            del self.focus_afflictions[name]

        self.unpredict(aff["name"])

        return True

    def clear_all_affs(self):
        self.active_afflictions = {}
        self.smoke_afflictions = {}
        self.pill_afflictions = {}
        self.poultice_afflictions = {}
        self.writhe_afflictions = {}
        self.focus_afflictions = {}
        self.predictions = []

    def predict(self, aff):
        if aff in self.predictions:
            return
        self.predictions.append(aff)
        self.mud.send("firstaid predict %s" % aff)

    def unpredict(self, aff):
        if aff in self.predictions:
            del self.predictions[aff]

    def parse_line(self, line):
        for trig in self.group_triggers:
            match = trig[0].match(line)
            if (match):
                trig[1](match.group(1))
                return
        for trig in self.triggers:
            match = trig[0].match(line)
            if (match):
                trig[1]()
                return
        for trig in self.predict_triggers:
            match = trig[0].match(line)
            if (match):
                for aff in trig[1]:
                    self.predict(aff)
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

    def get_focus(self):
        return self.focus_afflictions

    def __str__(self):
        return " ".join(self.active_afflictions.keys())
