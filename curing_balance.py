from core.spam_guard import SpamGuard
import re

class CuringBalance():

    def __init__(self, mud, **kwargs):
        self.mud = mud
        self.name = kwargs["name"]
        self.ready = True
        self.spam_guard = SpamGuard(2)
        self.fire_trigger = re.compile(kwargs["fire_trigger"])
        self.reset_trigger = re.compile(kwargs["reset_trigger"])
        self.busy_trigger = re.compile(kwargs["busy_trigger"])
        self.command = kwargs["command"]

    def parse_line(self, line):
        if self.fire_trigger.match(line) or self.busy_trigger.match(line):
            self.ready = False
            self.spam_guard.reset()
        elif self.reset_trigger.match(line):
            self.ready = True
            self.spam_guard.reset()

    def available(self):
        return self.ready and not self.spam_guard.locked()

    def use(self, item = ""):
        cmd = self.command % item
        if not self.available():
            return
        self.spam_guard.lock()
        self.mud.send(cmd)
