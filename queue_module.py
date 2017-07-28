from core.module import Module
from core.prompt_listener import PromptListener

class QueueModule(Module, PromptListener):

    def __init__(self, *args):
        super(QueueModule, self).__init__(*args)
        
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
        if not self.state["cmd_queue"]:
            return

        player = self.state["player"]
        balance = player["balance"] and player["equilibrium"]

        if balance:
            self.mud.send(self.state["cmd_queue"].popleft())
