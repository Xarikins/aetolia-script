from core.module import Module
from core.prompt_listener import PromptListener
from core.spam_guard import SpamGuard

class QueueModule(Module, PromptListener):

    def __init__(self, *args):
        super(QueueModule, self).__init__(*args)
        self.spam_guard = SpamGuard(1)
        
        self.state["alias_builder"].build({
            "cq": self.__clear_queue,
            })

        self.state["alias_builder"].build({
            "^q (.+)$": {
                "fun": self.__queue_cmd,
                "arg": "'%P1'",
                }
            }, "regexp")

    def __queue_cmd(self, cmd):
        self.state["cmd_queue"].append(cmd)
        self.mud.info("Queued cmd: %s" % cmd)

    def __clear_queue(self):
        self.state["cmd_queue"].clear()
        self.mud.info("Cleared command queue")

    def parse_prompt(self, line):
        self.trigger()

    def trigger(self):
        if not self.state["cmd_queue"]:
            return

        player = self.state["player"]
        balance = player["balance"] and player["equilibrium"]

        if balance and not self.spam_guard.locked():
            self.spam_guard.lock()
            cmd = self.state["cmd_queue"].popleft()
            self.mud.info("Popping cmd: %s" % cmd)
            self.mud.eval(cmd)
