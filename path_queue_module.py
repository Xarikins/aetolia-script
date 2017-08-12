from core.module import Module
from collections import deque

class PathQueueModule(Module):

    def __init__(self, *args):
        super(PathQueueModule, self).__init__(*args)

        self.commands = deque([])
        
        self.state["trigger_builder"].build({
            "^You have reached your destination\.$": self.pop_command,
            })

        self.state["alias_builder"].build({
            "mq *": {
                "fun": self.store_command,
                "arg": "'%2'",
                },
            "mqc": self.clear_queue,
            })

    def pop_command(self):
        if self.commands:
            cmd = self.commands.popleft()
            self.mud.info("Popping path command: %s" % cmd)
            self.mud.eval(cmd)

    def store_command(self, cmd):
        self.mud.info("Storing path command: %s" % cmd)
        self.commands.append(cmd)

    def clear_queue(self):
        self.mud.info("Clearing path move queue")
        self.commands = deque([])
