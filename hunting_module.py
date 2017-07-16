from threading import Timer
from core.module import Module

class HuntingModule(Module):

    def __init__(self, *args):
        super(HuntingModule, self).__init__(*args)
        self.attack_spamguard = False

        aBuilder = self.state["alias_builder"]
        aBuilder.build({
                "at": { "fun": self.at },
                "hunt": { "fun": self.toggle_bash },
            })

        gBuilder = self.state["gag_builder"]
        gBuilder.build({
            "^You will execute the following command when you next regain (.+)\\: (.+)$": {
                "fun": self.queued_command,
                "arg": "'%P1' '%P2'",
                }
            })

        tBuilder = self.state["trigger_builder"]
        tBuilder.build({
            "^You use Dhuriv .+ on .+\.$": self.registered_attack,
            "^You stand up and stretch your arms out wide\.$": self.registered_attack,
            })

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

    def __reset_attack_spamguard(self):
        self.attack_spamguard = False

    def registered_attack(self):
        if self.state["mode"]["bashing"] and not self.attack_spamguard:
            self.at()
            self.attack_spamguard = True
            Timer(1, self.__reset_attack_spamguard).start()


