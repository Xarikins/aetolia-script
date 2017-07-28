from core.module import Module
from core.prompt_listener import PromptListener
from message_client import MessageClient
import json

class GmcpModule(Module, PromptListener):

    client_data = {
        "Client": "TinyFugue",
        "Version": "6"
        }

    support_data = [
            "Core 1",
            "Char 1",
            "Room 1",
            "Comm.Channel 1",
            "Char.Afflictions 1",
            "Char.Defences 1",
            ]

    def __init__(self, *args):
        super(GmcpModule, self).__init__(*args)

        self.prompt_count = 0
        self.gmcp_count = 0
        self.message_client = MessageClient("localhost", 12000)

        self.mud.eval("/def -h'CONNECT aetolia' = /python_call main.cb register_gmcp")
        self.mud.eval("/def -waetolia -hGMCP = /python_call main.cb handle_gmcp '\%*'")
        self.state["callback_handler"].registerCallback(self.handle_gmcp)
        self.state["callback_handler"].registerCallback(self.register_gmcp)

    def parse_prompt(self, line):
        if self.gmcp_count:
            return
        self.prompt_count += 1
        if (self.prompt_count % 3) == 0:
            self.mud.warn("Received %d prompts and no GMCP" % self.prompt_count)
            self.register_gmcp()

    def register_gmcp(self):
        self.mud.info("Registering for GMCP")
        self.mud.eval('/test gmcp(\\"Core.Hello %s\\")' % json.dumps(self.client_data).replace("\"", "\\\\\""))
        self.mud.eval('/test gmcp(\\"Core.Supports.Set %s\\")' % json.dumps(self.support_data).replace("\"", "\\\\\""))

    def handle_gmcp(self, payload):
        self.gmcp_count += 1
        lines = payload.split(" ", 1)
        key = lines[0]
        package = lines[1]
        data = json.loads(package)
        if key == "Comm.Channel.Text":
            self.message_client.send(data["text"])
        else:
            self.state["gmcp"][key] = data
            self.update_state()

    def update_state(self):
        if not self.gmcp_count:
            return

        vitals = self.state["gmcp"]["Char.Vitals"]
        self.state["player"]["mounted"] = bool(int(vitals["mounted"]))
        self.state["player"]["writhing"] = bool(int(vitals["writhing"]))
