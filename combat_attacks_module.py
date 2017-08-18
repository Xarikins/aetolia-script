from core.module import Module
from core.prompt_listener import PromptListener
from core.spam_guard import SpamGuard

class CombatAttacksModule(Module, PromptListener):

    def __init__(self, *args):
        super(CombatAttacksModule, self).__init__(*args)

        self.auto_hit = False
        self.auto_hit_guard = SpamGuard(0.5)
        
        self.locking_affs = [
                ("paresis", "curare"),
                ("asthma", "kalmia"),
                ("clumsiness", "xentio"),
                ("slickness", "gecko"),
                ("anorexia", "slike"),
                ("stupidity", "aconite"),
                ("left_leg_broken", "epseth"),
                ("right_leg_broken", "epseth"),
                ("left_arm_broken", "epteth"),
                ("right_arm_broken", "epteth"),
                ]

        self.salve_affs = [
                ("left_leg_broken", "epseth"),
                ("right_leg_broken", "epseth"),
                ("left_arm_broken", "epteth"),
                ("right_arm_broken", "epteth"),
                ("paresis", "curare"),
                ("slickness", "gecko"),
                ("paresis", "curare"),
                ("asthma", "kalmia"),
                ("clumsiness", "xentio"),
                ]

        self.current_affs = self.locking_affs

        self.state["alias_builder"].build({
            "hit": self.hit,
            "raz": self.dualraze,
            "ah": self.toggle_auto_hit,
            "vlock": self.venom_lock,
            "spc": self.spinecut,
            "fsalve": self.use_salve_affs,
            "freg": self.use_locking_affs,
            })

    def use_salve_affs(self):
        self.mud.info("Using salve affliction scheme")
        self.current_affs = self.salve_affs

    def use_locking_affs(self):
        self.mud.info("Using locking affliction scheme")
        self.current_affs = self.locking_affs

    def toggle_auto_hit(self):
        self.auto_hit = not self.auto_hit
        self.mud.info("Auto hit %s" % ("enabled" if self.auto_hit else "disabled"))

    def get_afflictions(self):
        affs = self.state["combat"]["target_affs"]
        aff1 = ""
        aff2 = ""
        for affliction in self.current_affs:
            aff = affliction[0]
            if aff not in affs:
                if not aff1:
                    aff1 = affliction
                else:
                    aff2 = affliction
                    break

        return (aff1, aff2)

    def dualraze(self):
        self.mud.send("dhuriv dualraze %s" % self.state["combat"]["target"])

    def hit(self):
        affs = self.get_afflictions()
        if self.state["combat"]["target_rebounding"]:
            commands = [
                    "qeb wipe dhurive",
                    "envenom dhurive with %s" % affs[0][1],
                    "dhuriv combo %s reave stab" % self.state["combat"]["target"]
                    ]
            self.mud.send(";".join(commands))
        elif len(affs) > 1:
            commands = [
                    "qeb wipe dhurive",
                    "envenom dhurive with %s" % affs[1][1],
                    "envenom dhurive with %s" % affs[0][1],
                    "dhuriv combo %s slash stab" % self.state["combat"]["target"]
                    ]
            self.mud.send(";".join(commands))
        else:
            self.mud.send("dhuriv combo %s throatcrush heartbreaker" % self.state["combat"]["target"])
        
    def spinecut(self):
        self.mud.send("qeb dhuriv spinecut %s" % self.state["combat"]["target"])

    def venom_lock(self):
        target = self.state["combat"]["target"]
        commands1 = [
                "q wipe dhurive",
                "envenom dhurive with slike",
                "envenom dhurive with aconite",
                "dhuriv whirl %s" % target
                ]
        commands2 = [
                "q wipe dhurive",
                "envenom dhurive with gecko",
                "envenom dhurive with kalmia",
                "dhuriv combo %s slash stab" % target
                ]
        self.mud.eval(";".join(commands1))
        self.mud.eval(";".join(commands2))

    def parse_prompt(self, prompt):
        if not self.auto_hit:
            return

        if self.state["cmd_queue"]:
            return

        if self.auto_hit_guard.locked():
            return
        self.auto_hit_guard.lock()

        player = self.state["player"]
        eq = player["equilibrium"]
        ba = player["balance"]
        standing = not player["prone"]
        writhing = player["writhing"]
        writhe_affliction = any("writhe" in s for s in player["affs"])
        stun = "stun" in player["affs"]
        paralyzed = "paralysis" in player["affs"]

        if ba and eq and standing \
                and not paralyzed \
                and not writhing \
                and not writhe_affliction \
                and not stun:
                    self.hit()
