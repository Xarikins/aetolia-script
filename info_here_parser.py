import re

from core.module import Module
from core.line_listener import LineListener

class InfoParser(Module, LineListener):
    PATTERN = "^You can see the following (\d+) objects\\:$"
    CPATTERN = re.compile(PATTERN)

    VALID_TARGETS = [
            "forager",
            "hunter",
            "lumberjack",
            "umbra",
            "priest",
            "syll",
            "boru",
            "boar",
            "nazetu",
            "shark",
            "crab",
            ]

    def __init__(self, combat_module, *args):
        super(InfoParser, self).__init__(*args)
        self.running = False
        self.count = 0
        self.combat_module = combat_module

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
        if self.__check_target(line):
            self.count = 0

        if not self.count:
            self.running = False

    def __check_target(self, line):
        for tar in InfoParser.VALID_TARGETS:
            if line.startswith(tar, 1):
                self.combat_module.target(line.split()[0].strip('"'))
                return True

        return False

