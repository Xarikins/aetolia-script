from core.module import Module

class MountModule(Module):

    def __init__(self, *args):
        super(MountModule, self).__init__(*args)

        self.state["alias_builder"].build({
            "ms": self.mount_steed,
            "dis": self.dismount,
            "wolf": "recall 18597",
            "returnm": "return mount duiranstable",
            })


    def mount_steed(self):
        if not self.state["player"]["mounted"]:
            self.mud.send(";".join(["recall mount","qmount 18597"]))

    def dismount(self):
        if self.state["player"]["mounted"]:
            self.mud.send("qdmount")

