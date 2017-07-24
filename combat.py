from threading import Timer
import re

from core.module import Module

class CombatModule(Module):
    def __init__(self, *args, **kwargs):
        super(CombatModule, self).__init__(*args, **kwargs)

        ALIASES_REG = {
                # Target alias
                "^x (.+)$": { "fun": self.target, "arg": "%P1" }
                }
        ALIASES_GLOB = {
                # Bashing aliases
                "slsl": { "fun": self.slam_slit },
                "fight": { "fun": self.toggle_fight },
                "oek": { "fun": self.oek },
                "oep": "qeb order entourage passive",
                "ca": "call animals",
                "targetlisten": self.toggle_target_listening,

                # Tracking aliases
                "no *": "outc 2 rope;lay noose %2",
                "spike": "outc 1 rope;outc 1 wood;outc 1 iron;lay spike here",
                "launch": "outc 1 rope;outc 1 wood;lay launcher here",
                "dis *": "disarm trap %2",
                "sh *": { "fun": self.shoot, "arg": "%2" },
                "qs": self.quickshot,
                "ct": "qeb crossbow targets",
                "sh": self.snipe,
                "resin *": {"fun": self.set_resin, "arg": "%2"},
                "noresin": self.no_resin,
                "ts": "qeb touch shield",
                "en *": "enemy %2",
                "en": self.enemy_target,
                "unen *": "unenemy %2",
                }

        aBuilder = self.state["alias_builder"]
        aBuilder.build(ALIASES_REG, "regexp")
        aBuilder.build(ALIASES_GLOB)

        self.resin = "harimel"
        self.venom1 = ""
        self.venom2 = ""
        self.target_listening = False

        tBuilder = self.state["trigger_builder"]
        tBuilder.build({
            "^\(.*\)\: \w+ says, \"Target\: (.+)\.\"$": {
                "fun": self.target,
                "arg": "%P1",
                },
            })

    def no_resin(self):
        self.set_resin()

    def set_resin(self, resin = ""):
        self.resin = resin
        self.mud.info("Resin: %s" % self.resin)

    def set_venoms(self, v1, v2):
        self.set_venom1(v1)
        self.set_venom2(v1)

    def set_venom_1(self, venom):
        self.venom1 = venom
        self.mud.info("Venom 1: %s" % self.venom1)

    def set_venom_2(self, venom):
        self.venom2 = venom
        self.mud.info("Venom 2: %s" % self.venom2)

    def load_crossbow(self):
        msg = "qeb crossbow load with normal"
        if (self.resin):
            msg += " coat %s" % self.resin
        self.mud.send(msg)

    def oek(self):
        self.mud.send("qeb order entourage kill %s" % self.state["combat"]["target"])

    def shoot(self, direction):
        self.load_crossbow()
        self.mud.send("qeb crossbow shoot %s %s" % (self.state["combat"]["target"], direction))

    def snipe(self):
        self.load_crossbow()
        self.mud.send("qeb crossbow shoot %s" % self.state["combat"]["target"])

    def quickshot(self):
        self.load_crossbow()
        self.mud.send("qeb crossbow quickshoot %s" % self.state["combat"]["target"])

    def slam_slit(self):
        attack = "/send qeb dhuriv combo %s slam slit" % self.state["combat"]["target"]
        self.mud.eval(attack)

    def toggle_fight(self):
        self.state["mode"]["fight"] = not self.state["mode"]["fight"]
        self.mud.info("Fightmode %s" % ("enabled" if self.state["mode"]["fight"] else "disabled"))

    def toggle_target_listening(self):
        self.target_listening = not self.target_listening
        self.mud.info("Target listening enabled" if self.target_listening else "Target listening disabled")

    def target(self, target):
        self.state["combat"]["target"] = target
        if target:
            self.mud.info("Current target: %s" % self.state["combat"]["target"])

    def enemy_target(self):
        self.mud.send("enemy %s" % self.state["combat"]["target"])
