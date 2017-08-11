import re
from threading import Timer

from core.module import Module
from core.line_listener import LineListener
from core.spin_lock import SpinLock

class InfoParser(Module, LineListener):
    PATTERN = "^You can see the following (\d+) objects\\:$"
    CPATTERN = re.compile(PATTERN)
    NOTHING_PATTERN = "^There is nothing here\.$"
    CNOTHING_PATTERN = re.compile(NOTHING_PATTERN)


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
            "Nazetu": 0,
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
            "apparition": 0,
            "spirit": 0,
            "shade": 10,
            "luminary": 10,
            "darkwalker": 10,
            "rojalli": 0,
            "spirit": 0,
            "rat": 0,
            "lichosphere": 0,
            }

    def __init__(self, *args):
        super(InfoParser, self).__init__(*args)
        self.running = False
        self.count = 0
        self.prio = -1
        self.selected_target = ""

    def parse_line(self, line):
        if not self.state["mode"]["bashing"]:
            return

        match = InfoParser.CNOTHING_PATTERN.match(line)
        if match:
            self.complete()
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

        if not self.count:
            self.complete()

    def complete(self):
        self.running = False
        if self.selected_target:
            self.mud.eval("x %s" % self.selected_target)

        self.selected_target = ""
        self.prio = -1

        self.mud.eval("at")

    def __check_target(self, line):
        for tar, prio in InfoParser.VALID_TARGETS.items():
            if line.startswith(tar, 1) and prio > self.prio:
                self.selected_target = line.split()[0].strip('"')
                self.prio = prio

