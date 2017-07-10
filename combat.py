import imp

from core.module import Module
from core.line_listener import LineListener

class CombatModule(Module, LineListener):
    def __init__(self, *args, **kwargs):
        super(CombatModule, self).__init__(*args, **kwargs)

        ALIASES_REG = {
                # Target alias
                "^x ([\\\w\\\d]+)\\$": { "fun": self.target, "arg": "%1" }
                }
        ALIASES_GLOB = {
                # Bashing aliases
                "at": { "fun": self.at, "arg": "" },
                "hunt": { "fun": self.toggle_bash, "arg": "" }
                }

        builder = self.state["alias_builder"]
        builder.build(ALIASES_REG, "regexp")
        builder.build(ALIASES_GLOB)

    def at(self, arg):
        attack = "/send dhuriv combo %s slash stab" % self.state.combat["target"]
        tf.eval(attack)
        if self.state["mode"]["bashing"]:
            self.state["command_queue"].append(attack)

    def toggle_bash(self, arg):
        self.state["mode"]["bashing"] = not self.state["mode"]["bashing"]
        print("Bashing %s" % ("enabled" if self.state["mode"]["bashing"] else "disabled"))

    def target(self, target):
        self.state["combat"]["target"] = target
        print("Current target: %s" % self.state["combat"]["target"])

    def parse_line(self, line):
        pass
