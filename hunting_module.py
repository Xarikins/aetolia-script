from core.module import Module
from core.prompt_listener import PromptListener
from core.spam_guard import SpamGuard

import path

class HuntingModule(Module, PromptListener):

    def __init__(self, *args):
        super(HuntingModule, self).__init__(*args)

        self.attack_spamguard = SpamGuard(2)
        self.step_spamguard = SpamGuard(0.2)
        self.notarget_spamguard = SpamGuard(0.2)

        self.path = path.Path(self.mud)
        self.next_move = None

        aBuilder = self.state["alias_builder"]
        aBuilder.build({
                "at": { "fun": self.at },
                "hunt": { "fun": self.toggle_bash },
                "loadpath *": {
                    "fun": self.load_path,
                    "arg": "%2"
                    },
                "clearpath": self.path.clear,
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
            "^You can find no such target as '(.*)'\.$": {
                "fun": self.no_target_found,
                "arg": "%P1",
                },
            "^The final blow proves too much for .+$": self.registered_kill,
            "^(A .+) snarls angrily at you and moves in for the kill\.$": aggro_definition,
            "^(An .+) snarls angrily at you and moves in for the kill\.$": aggro_definition,
            "^Your vision distorts briefly, light scattering subtly as ylem energy diffuses into the surrounding atmosphere\.$": self.registered_ylem,
            })

        self.state["trigger_builder"].build({
            "^You use Dhuriv .+ on .+\.$": self.registered_attack,
            })

    def parse_prompt(self, line):
        if not self.state["mode"]["bashing"] or not self.next_move:
            return

        player = self.state["player"]
        eq = player["equilibrium"]
        ba = player["balance"]
        standing = not player["prone"]
        writhing = player["writhing"]
        writhe_affliction = any("writhe" in s for s in player["affs"])
        stun = "stun" in player["affs"]
        paralyzed = "paralysis" in player["affs"]

        if ba and eq and standing \
                and self.next_move \
                and not paralyzed \
                and not writhing \
                and not writhe_affliction \
                and not stun:
            self.next_move()

    def check_for_target(self):
        self.next_move = None
        self.mud.send("info here")

    def registered_kill(self):
        if self.state["mode"]["bashing"] and not self.next_move:
            self.mud.info("Checking for new target")
            self.next_move = self.check_for_target

    def no_target_found(self, target):
        self.mud.info("No target: %s" % target)
        if not self.notarget_spamguard.locked():
            self.notarget_spamguard.lock()
            self.next_move = self.check_for_target
        else:
            self.next_move = self.auto_step

    def registered_attack(self):
        if self.state["mode"]["bashing"]:
            self.next_move = self.auto_at

    def aggro_warn(self, attacker):
        self.mud.warn("Aggro by %s" % attacker)

    def auto_step(self):
        if self.path.has_step() and not self.step_spamguard.locked():
            self.step_spamguard.lock()
            step = self.path.get_next()
            self.mud.info("Auto stepping, %d steps left" % len(self.path))
            self.mud.eval("ms")
            self.mud.send(step)
            self.mud.send("info here")
            self.next_move = None

    def auto_at(self):
        if not self.attack_spamguard.locked():
            self.attack_spamguard.lock()
            self.next_move = None
            self.mud.info("Auto attacking")
            self.at()

    def at(self):
        attack = "/send qeb dhuriv combo %s throatcrush heartbreaker" % self.state["combat"]["target"]
        self.notarget_spamguard.reset()
        self.mud.eval(attack)

    def toggle_bash(self):
        self.state["mode"]["bashing"] = not self.state["mode"]["bashing"]
        self.mud.info("Bashing %s" % ("enabled" if self.state["mode"]["bashing"] else "disabled"))
        self.mud.eval("/set bashing=%d" % int(self.state["mode"]["bashing"]))

    def queued_command(self, queue, command):
        if "balance" in queue and "equilibrium" in queue:
            self.mud.info("QEB: %s" % command)
        elif balance in queue:
            self.mud.info("QB: %s" % command)
        elif equilibrium in queue:
            self.mud.info("QE: %s" % command)

    def load_path(self, name):
        self.path.load(name)

    def registered_ylem(self):
        self.mud.info("Absorbing ylem next")
        self.next_move = self.absorb_ylem

    def absorb_ylem(self):
        self.mud.send("absorb ylem")
        self.next_move = self.check_for_target
