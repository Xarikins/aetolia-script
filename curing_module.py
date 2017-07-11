import json
from threading import Timer

from focus_cure import FocusCure
from tree_cure import TreeCure

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

    def parse_line(self, line):
        self.afflictions.parse_line(line)
        self.focus.parse_line(line)

    def parse_prompt(self, prompt):
        self.__cure()

    def __cure(self):
        pill_affs = self.afflictions.get_pill()
        smoke_affs = self.afflictions.get_smoke()
        poultice_affs = self.afflictions.get_poultice()
        writhe_affs = self.afflictions.get_writhe()

        cure_count = 0
