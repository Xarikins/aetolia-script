import json
from threading import Timer

from focus_cure import FocusCure
from tree_cure import TreeCure
from pill_cure import PillCure
from smoke_cure import SmokeCure
from salve_cure import PoulticeCure
from erase_cure import EraseCure
from special_cure import SpecialCure

from affliction_container import AfflictionContainer
from defences_container import DefencesContainer
from core.module import Module
from core.line_listener import LineListener
from core.prompt_listener import PromptListener

class CuringModule(Module, LineListener, PromptListener):

    def __init__(self, *args):
        super(CuringModule, self).__init__(*args)
        self.afflictions = AfflictionContainer(self.state["settings"]["afflictions_file"])
        self.defences = DefencesContainer(self.state)
        self.focus = FocusCure(self.state["communicator"])
        self.tree = TreeCure(self.state["communicator"])
        self.pill = PillCure(self.state["communicator"])
        self.smoke = SmokeCure(self.state["communicator"])
        self.poultice = PoulticeCure(self.state["communicator"])
        self.erase = EraseCure(self.state["communicator"])
        self.special = SpecialCure(self.state["communicator"])
        self.cure_delays = {}
        self.enabled = False

    def parse_line(self, line):
        self.afflictions.parse_line(line)
        self.defences.parse_line(line)
        self.focus.parse_line(line)

    def parse_prompt(self, prompt):
        if self.state["player"]["health"] == 0:
            return

        if self.enabled:
            self.__cure()
        self.__cure_defs()
        self.__update_state()

    def __update_state(self):
        afflist = self.afflictions.get_active().keys()
        deflist = list(map(lambda x: x["name"], self.defences.get_missing()))
        self.state["player"]["affs"] = afflist
        self.state["player"]["missing_defs"] = deflist

    def __cure(self):
        active_affs = self.afflictions.get_active()
        pill_affs = self.afflictions.get_pill()
        smoke_affs = self.afflictions.get_smoke()
        poultice_affs = self.afflictions.get_poultice()
        writhe_affs = self.afflictions.get_writhe()

        cure_count = 0
        if pill_affs and self.pill.available():
            self.mud.send("outc %s" % self.__priority_aff(pill_affs)["pill"])
            self.pill.use(self.__priority_aff(pill_affs)["pill"])
            cure_count += 1
        if smoke_affs and self.smoke.available():
            self.smoke.use(self.__priority_aff(smoke_affs)["smoke"])
            cure_count += 1
        if poultice_affs and self.poultice.available():
            command = self.__priority_aff(poultice_affs)["poultice"]
            if "body_part" in poultice_affs[0]:
                command += " " + self.__priority_aff(poultice_affs)["body_part"]
            self.poultice.use(command)
            cure_count += 1
        if writhe_affs and self.writhe.avilable():
            cure_count += 1
            pass

        if (len(active_affs) - cure_count) > 2:
            self.tree.use()
            self.erase.use()
            self.focus.use()
        elif (len(active_affs) - cure_count) > 1:
            self.tree.use()
            self.erase.use()
        elif (len(active_affs) - cure_count == 1):
            self.tree.use()

    def __cure_defs(self):
        missing = self.defences.get_missing()
        if not missing or self.afflictions.get_active() or self.state["cmd_queue"]:
            return

        ba = self.state["player"]["balance"]
        eq = self.state["player"]["equilibrium"]
        full_balance = ba and eq
        balance_cmd_sent = False

        for defence in missing:
            if defence["pill"] and self.pill.available() and not self.__cure_delay(defence):
                self.mud.send("outc %s" % defence["pill"])
                self.pill.use(defence["pill"])
            elif defence["poultice"] and self.poultice.available() and not self.__cure_delay(defence):
                self.poultice.use(defence["poultice"])
            elif defence["smoke"] and self.smoke.available() and not self.__cure_delay(defence):
                self.smoke.use(defence["smoke"])
            elif defence["special"] and not self.__cure_delay(defence):
                if defence["balance_required"] and not balance_cmd_sent and full_balance:
                    self.special.use(defence["special"])
                    balance_cmd_sent = defence["balance_take"]
                elif not defence["balance_required"]:
                    self.special.use(defence["special"])

    def __cure_delay(self, aff):
        if aff["name"] in self.cure_delays:
            return True
        
        if aff["cure_delay"]:
            self.cure_delays[aff["name"]] = True
            Timer(aff["cure_delay"], self.__remove_cure_delay, [aff["name"]]).start()
            return False
        else:
            return False

    def __remove_cure_delay(self, name):
        del self.cure_delays[name]

    def __priority_aff(self, data):
        return data[list(data)[0]]
