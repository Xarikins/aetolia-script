import imp

from core.module import Module
from core.line_listener import LineListener

class CombatModule(Module, LineListener):
    def __init__(self, *args, **kwargs):
        super(CombatModule, self).__init__(*args, **kwargs)

        ALIASES_REG = {
                # Target alias
                "^x ([\\\w\\\d]+)\\$": { "fun": self.target, "arg": "%P1" }
                }
        ALIASES_GLOB = {
                # Bashing aliases
                "at": { "fun": self.at },
                "hunt": { "fun": self.toggle_bash },
                "fight": { "fun": self.toggle_fight },
                "oek": { "fun": self.oek },
                "oep": "order entourage passive",
                "ca": "call animals",
                }

        builder = self.state["alias_builder"]
        builder.build(ALIASES_REG, "regexp")
        builder.build(ALIASES_GLOB)

    def oek(self):
        self.state["communicator"].send("order entourage kill %s" % self.state["combat"]["target"])

    def at(self):
        attack = "/send dhuriv combo %s slash stab" % self.state["combat"]["target"]
        self.state["communicator"].eval(attack)

    def toggle_bash(self):
        self.state["mode"]["bashing"] = not self.state["mode"]["bashing"]
        print("Bashing %s" % ("enabled" if self.state["mode"]["bashing"] else "disabled"))

    def toggle_fight(self):
        self.state["mode"]["fight"] = not self.state["mode"]["fight"]
        print("Fightmode %s" % ("enabled" if self.state["mode"]["fight"] else "disabled"))

    def target(self, target):
        self.state["combat"]["target"] = target
        print("Current target: %s" % self.state["combat"]["target"])

    def parse_line(self, line):
        pass
