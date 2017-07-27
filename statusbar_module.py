from core.module import Module
from core.prompt_listener import PromptListener

class StatusBarModule(Module, PromptListener):

    def __init__(self, *args):
        super(StatusBarModule, self).__init__(*args)

    def parse_prompt(self, line):
        self.mud.eval("/set fighting=%d" % int(self.state["mode"]["fight"]))
        self.mud.eval("/set bashing=%d" % int(self.state["mode"]["bashing"]))
        self.mud.eval("/set active_affs=%s" % " ".join(self.state["player"]["affs"]))
        self.mud.eval("/set missing_defs=%s" % " ".join(self.state["player"]["missing_defs"]))
