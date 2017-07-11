import json
from threading import Timer

from focus_cure import FocusCure
from tree_cure import TreeCure
from pill_cure import PillCure
from smoke_cure import SmokeCure
from salve_cure import PoulticeCure

from affliction_container import AfflictionContainer
from core.module import Module
from core.line_listener import LineListener
from core.prompt_listener import PromptListener

class CuringModule(Module, LineListener, PromptListener):

    def __init__(self, *args):
        super(CuringModule, self).__init__(*args)
        self.afflictions = AfflictionContainer()
        self.focus = FocusCure(self.state["communicator"])
        self.tree = TreeCure(self.state["communicator"])
        self.pill = PillCure(self.state["communicator"])
        self.smoke = SmokeCure(self.state["communicator"])
        self.poultice = PoulticeCure(self.state["communicator"])
        self.enabled = False

    def parse_line(self, line):
        self.afflictions.parse_line(line)
        self.focus.parse_line(line)

    def parse_prompt(self, prompt):
        if self.enabled:
            self.__cure()

    def __cure(self):
        active_affs = self.afflictions.get_active()
        pill_affs = self.afflictions.get_pill()
        smoke_affs = self.afflictions.get_smoke()
        poultice_affs = self.afflictions.get_poultice()
        writhe_affs = self.afflictions.get_writhe()

        cure_count = 0
        if pill_affs and self.pill.available():
            self.state["communicator"].send("outc %s" % self.__priority_aff(pill_affs)["pill"])
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

        if (len(active_affs) - cure_count) > 1:
            self.tree.use()
            self.focus.use()
        elif (len(active_affs) - cure_count == 1):
            self.tree.use()

    def __priority_aff(self, data):
        return data[list(data)[0]]
