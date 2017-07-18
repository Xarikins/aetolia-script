from threading import Timer
from core.module import Module
from core.prompt_listener import PromptListener

class HuntingModule(Module, PromptListener):

    def __init__(self, *args):
        super(HuntingModule, self).__init__(*args)
        self.attack_spamguard = False
        self.attack_ready = False

        aBuilder = self.state["alias_builder"]
        aBuilder.build({
                "at": { "fun": self.at },
                "hunt": { "fun": self.toggle_bash },
            })

        aggro_definition = {
                "fun": self.aggro_warn,
                "arg": "'%P1'",
                }

        gBuilder = self.state["gag_builder"]
        gBuilder.build({
            "^You will execute the following command when you next regain (.+)\: (.+)$": {
                "fun": self.queued_command,
                "arg": "'%P1' '%P2'",
                },
            "^The final blow proves too much for .+$": self.check_for_target,
            "^(A .+) snarls angrily at you and moves in for the kill\.$": aggro_definition,
            "^(An .+) snarls angrily at you and moves in for the kill\.$": aggro_definition,
            })

        tBuilder = self.state["trigger_builder"]
        tBuilder.build({
            "^You use Dhuriv .+ on .+\.$": self.registered_attack,
            })

    def parse_prompt(self, line):
        if not self.state["mode"]["bashing"] or not self.attack_ready:
            return

        player = self.state["player"]
        eq = player["equilibrium"]
        ba = player["balance"]
        standing = not player["prone"]
        paralyzed = "paralysis" in player["affs"]

        if ba and eq and standing and not paralyzed:
            self.auto_at()

    def check_for_target(self):
        self.mud.send("info here")
        self.mud.info("Checking for new target")

    def registered_attack(self):
        self.attack_ready = True

    def __reset_attack_spamguard(self):
        self.attack_spamguard = False

    def aggro_warn(self, attacker):
        self.mud.warn("Aggro by %s" % attacker)

    def auto_at(self):
        if not self.attack_spamguard:
            self.attack_spamguard = True
            self.attack_ready = False
            Timer(2, self.__reset_attack_spamguard).start()
            self.mud.info("Auto attacking")
            self.at()

    def at(self):
        attack = "/send qeb dhuriv combo %s throatcrush heartbreaker" % self.state["combat"]["target"]
        self.mud.eval(attack)

    def toggle_bash(self):
        self.state["mode"]["bashing"] = not self.state["mode"]["bashing"]
        self.mud.info("Bashing %s" % ("enabled" if self.state["mode"]["bashing"] else "disabled"))

    def queued_command(self, queue, command):
        if "balance" in queue and "equilibrium" in queue:
            self.mud.info("QEB: %s" % command)
        elif balance in queue:
            self.mud.info("QB: %s" % command)
        elif equilibrium in queue:
            self.mud.info("QE: %s" % command)
