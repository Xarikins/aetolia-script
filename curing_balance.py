import re
from threading import Timer

class CuringBalance():

    def __init__(self, mud, **kwargs):
        self.mud = mud
        self.name = kwargs["name"]
        self.ready = True
        self.spam_guard = False
        self.fire_trigger = re.compile(kwargs["fire_trigger"])
        self.reset_trigger = re.compile(kwargs["reset_trigger"])
        self.busy_trigger = re.compile(kwargs["busy_trigger"])
        self.command = kwargs["command"]

    def parse_line(self, line):
        if self.fire_trigger.match(line) or self.busy_trigger.match(line):
            self.avilable = False
            self.spam_guard = False
        elif self.reset_trigger.match(line):
            self.ready = True
            self.spam_guard = False

    def available(self):
        return self.ready and not self.spam_guard

    def use(self, item = ""):
        if not self.available():
            return
        cmd = self.command % item
        print("Sending: %s" % cmd)
        self.mud.send(cmd)

    def __spam_guard(self):
        self.spam_guard = True
        t = Timer(2, self.__reset_spam_guard)
        t.start()

    def __reset_spam_guard(self):
        self.spam_guard = False
