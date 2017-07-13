import re

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
                "slsl": { "fun": self.slam_slit },
                "hunt": { "fun": self.toggle_bash },
                "fight": { "fun": self.toggle_fight },
                "oek": { "fun": self.oek },
                "oep": "order entourage passive",
                "ca": "call animals",
                "targetlisten": self.toggle_target_listening,

                # Tracking aliases
                "no *": "outc 2 rope;lay noose \%2",
                "spike": "outc 1 rope;outc 1 wood;outc 1 iron;lay spike here",
                "launch": "outc 1 rope;outc 1 wood;lay launcher here",
                "dis *": "disarm trap \%2",
                }

        builder = self.state["alias_builder"]
        builder.build(ALIASES_REG, "regexp")
        builder.build(ALIASES_GLOB)

        self.target_listening = False
        self.triggers = {
                "target": re.compile("^\(.*\)\: \w+ says, \"Target\: (\w+)\"$"),
                }

    def oek(self):
        self.mud.send("order entourage kill %s" % self.state["combat"]["target"])

    def slam_slit(self):
        attack = "/send dhuriv combo %s slam slit" % self.state["combat"]["target"]
        self.mud.eval(attack)

    def at(self):
        attack = "/send dhuriv combo %s slash thrust" % self.state["combat"]["target"]
        self.mud.eval(attack)

    def toggle_bash(self):
        self.state["mode"]["bashing"] = not self.state["mode"]["bashing"]
        print("Bashing %s" % ("enabled" if self.state["mode"]["bashing"] else "disabled"))

    def toggle_fight(self):
        self.state["mode"]["fight"] = not self.state["mode"]["fight"]
        print("Fightmode %s" % ("enabled" if self.state["mode"]["fight"] else "disabled"))

    def toggle_target_listening(self):
        self.target_listening = not self.target_listening
        self.mud.out("Target listening enabled" if self.target_listening else "Target listening disabled")

    def target(self, target):
        self.state["combat"]["target"] = target
        print("Current target: %s" % self.state["combat"]["target"])

    def parse_line(self, line):
        match = self.triggers["target"].match(line)
        if match:
            self.target(match.group(1))
