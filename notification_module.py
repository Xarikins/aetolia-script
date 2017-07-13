import subprocess
import re

from core.module import Module
from core.line_listener import LineListener

class NotificationModule(Module, LineListener):

    def __init__(self, *args):
        super(NotificationModule, self).__init__(*args)
        self.mud = self.state["communicator"]

        self.triggers = []
        self.triggers.append(re.compile("^(\(.+\))\: (.*)$"))

    def parse_line(self, line):
        for trigger in self.triggers:
            match = trigger.match(line)
            if match:
                subprocess.Popen(["notify-send", "-t", "4", "-i", "/home/linus/muds/aetolia/aet_notify_icon.png", "Aetolia", "%s %s" % (match.group(1), match.group(2))])

