from core.module import Module

class WieldModule(Module):

    def __init__(self, *args):
        super(WieldModule, self).__init__(*args)
        self.left_hand = ""
        self.right_hand = ""
        
        self.state["alias_builder"].build({

            # Weapons
            "dhurive": {
                "fun": self.wield,
                "arg": "dhurive",
                },
            "sickle": {
                "fun": self.wield,
                "arg": "sickle",
                }
        })

        self.state["callback_handler"].registerGmcpCallback("Char.Vitals", self.update)

    def update(self, data):
        left = data["wield_left"]
        right = data["wield_right"]

        self.left_hand = left if left != "empty" else ""
        self.right_hand = right if right != "empty" else ""

    def wield(self, item):
        command = []
        if self.left_hand:
            command.append("secure %s" % self.left_hand)
        if self.right_hand:
            command.append("secure %s" % self.right_hand)

        command.append("wield %s" % item)
        self.mud.send(";".join(command))


