import re

from core.module import Module
from core.line_listener import LineListener

class InfoParser(Module, LineListener):
    PATTERN = "^You can see the following (\d+) objects\\:$"
    CPATTERN = re.compile(PATTERN)

    VALID_TARGETS = {
            "forager": 0,
            "hunter": 0,
            "lumberjack": 0,
            "umbra": 0,
            "priest": 0,
            "syll": 0,
            "boru": 0,
            "boar": 10,
            "nazetu": 0,
            "shark": 10,
            "crab": 0,
            "eld": 0,
            "ogre": 10,
            "berserker": 10,
            "grimshrill": 0,
            "construct": 0,
            "basilwyrm": 0,
            "garwhol": 10,
            "knight": 0,
            "phenkyre": 10,
            "chempala": 0,
            "lumore": 0,
            "invoker": 0,
            "argobole": 10,
            }

    def __init__(self, combat_module, *args):
        super(InfoParser, self).__init__(*args)
        self.running = False
        self.count = 0
        self.combat_module = combat_module
        self.prio = -1
        self.selected_target = ""

    def parse_line(self, line):
        if not self.state["mode"]["bashing"]:
            return

        match = InfoParser.CPATTERN.match(line)
        if match:
            self.running = True
            self.count = int(match.group(1))
            return

        if not self.running:
            return

        self.count -= 1
        self.__check_target(line)

        if self.count:
            return

        self.running = False
        if self.selected_target:
            self.combat_module.target(self.selected_target)

        self.selected_target = ""
        self.prio = -1

    def __check_target(self, line):
        for tar, prio in InfoParser.VALID_TARGETS.items():
            if line.startswith(tar, 1) and prio > self.prio:
                self.selected_target = line.split()[0].strip('"')
                self.prio = prio

