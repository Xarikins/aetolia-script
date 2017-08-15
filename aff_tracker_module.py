from core.module import Module
from core.prompt_listener import PromptListener
from core.spam_guard import SpamGuard
from affliction_container import AfflictionContainer

class AffTrackerModule(Module, PromptListener):

    AFFLICTION_MANIPULATORS = [
            None,
            (" ", ""),
            (" ", "-"),
            (" ", "_")
            ]

    DHURIV_AFFLICTIONS = {
            "slam": ["epilepsy", "indifference"],
            "slit": ["crippled_throat"],
            "twirl": ["confusion"],
            "crosscut": ["haemophilia"],
            "weaken": ["lethargy"],
            "throatcrush": ["destroyed_throat"],
            "heartbreaker": ["heartflutter"],
            "gouge": ["impatience"],
            }

    def __init__(self, *args):
        super(AffTrackerModule, self).__init__(*args)
        self.target_afflictions = {}
        self.target_rebounding = {}
        self.ignore_next_venom = False
        self.rebounding_ignore_guard = SpamGuard(1)
        
        self.state["alias_builder"].build({
            "tclear": self.clear_target_affs,
            })

        self.state["gag_builder"].build({
            "^(\w+) presses \w+ (\w+) poultice against \w+ (.+), rubbing the poultice into \w+ flesh\.$": {
                "fun": self.__register_poultice,
                "arg": "'%P2' '%P1' '%P3'",
                },
            "^(\w+) takes a long drag off \w+ pipe filled with (\w+)\.$": {
                "fun": self.__register_smoke,
                "arg": "'%P2' '%P1'",
                },
            "^(\w+) swallows .+ (\w+) pill\.$": {
                "fun": self.__register_pill,
                "arg": "'%P2' '%P1'",
                },
            "^You discern that a layer of (\w+) has rubbed off your weapon\.$": {
                "fun": self.venom_afflict,
                "arg": "'%P1'",
                },
            "^A look of extreme focus crosses the face of (\w+)\.$": {
                "fun": self.register_focus,
                "arg": "'%P1'",
                },
            "^The attack rebounds back onto you!$": self.rebounding,
            "^(\w+)'s aura of weapons rebounding disappears\.$": {
                "fun": self.rebounding_toggle,
                "arg": "%P1 down",
                },
            "^You suddenly perceive the vague outline of an aura of rebounding around (\w+)\.$": {
                "fun": self.rebounding_toggle,
                "arg": "%P1 up",
                },
            })
        self.state["trigger_builder"].build({
            "^You discern that (\w+) has cured the effects of (.+)\.$": {
                "fun": self.__clear_aff,
                "arg": "'%P2' '%P1'",
                },
            "^You discern that (\w+) has resisted the (.+) affliction\.$": {
                "fun": self.__clear_aff,
                "arg": "'%P2' '%P1'",
                },
            "^Your \w+ has afflicted (\w+) with (.+)\.$": \
                self.__trigger_definition("'%P2' '%P1'"),
            "^(\w+) suddenly seizes up, \w+ entire body locked by paralysis\.$": \
                self.__trigger_definition("paralysis '%P1'"),
            "^You use Dhuriv (\w+) on (\w+)\.$": {
                "fun": self.__trigger_dhuriv_attack,
                "arg": "'%P1' '%P2'",
                },
            }, prio=2)

    def __trigger_dhuriv_attack(self, attack, target):
        attack = attack.lower()
        if not attack in self.DHURIV_AFFLICTIONS:
            return
        for aff in self.DHURIV_AFFLICTIONS[attack]:
            self.__register_aff(aff, target)

    def __trigger_definition(self, args):
        return {
                "fun": self.__register_aff,
                "arg": args,
                }

    def __get_affs_for(self, target):
        target = target.lower()
        if not target in self.target_afflictions:
            self.target_afflictions[target] = AfflictionContainer(self.state["settings"]["afflictions_file"])
        return self.target_afflictions[target]

    def rebounding(self):
        self.mud.warn("REBOUNDING")
        self.target_rebounding[self.state["combat"]["target"].lower()] = True
        if not self.rebounding_ignore_guard.locked():
            self.rebounding_ignore_guard.lock()
            self.ignore_next_venom = True

    def rebounding_toggle(self, target, status):
        if status == "up":
            self.mud.warn("Rebounding around: %s" % target)
            self.target_rebounding[target.lower()] = True
        else:
            self.mud.warn("Rebounding down: %s" % target)
            self.target_rebounding[target.lower()] = False

        if target == self.state["combat"]["target"]:
            self.state["combat"]["target_rebounding"] = status == "up"

    def register_focus(self, target):
        affs = self.__get_affs_for(target)
        for a in affs.get_active():
            if a["type"]["mental"]:
                self.__clear_aff(a["name"], target, "Focusing")
                return

    def __register_pill(self, pill, target):
        affs = self.__get_affs_for(target)
        if affs and affs.get_pill():
            for a in affs.get_pill().values():
                if a["pill"] == pill:
                    self.__clear_aff(a["name"], target, "Pill: %s" % pill)
                    return

    def __register_poultice(self, poultice, target, limb = ""):
        affs = self.__get_affs_for(target)

        original_limb = limb
        if limb == "skin" or limb == "flesh":
            limb = ""
        else:
            limb += "."

        if affs and affs.get_poultice():
            for a in affs.get_poultice().values():
                if a["poultice"] == poultice and a["body_part"] == limb:
                    self.__clear_aff(a["name"], target, "Poultice: %s on %s" % (poultice, original_limb))
                    return

    def __register_smoke(self, herb, target):
        affs = self.__get_affs_for(target)
        if affs and affs.get_smoke():
            for a in affs.get_smoke().values():
                if a["smoke"] == herb:
                    self.__clear_aff(a["name"], target, "Smoke: %s" % herb)
                    return

    def __clear_aff(self, aff, target, effect=""):
        target_affs = self.__get_affs_for(target)
        affliction_deregistered = False
        for i in self.AFFLICTION_MANIPULATORS:
            if i == None:
                affliction_deregistered = target_affs.deactivate(aff)
            else:
                affliction_deregistered = target_affs.deactivate(aff.replace(i[0], i[1]))

            if affliction_deregistered:
                break

        self.__print_target_affs(target, effect)

    def __register_aff(self, aff, target, effect=""):
        target = target.lower()

        target_affs = self.__get_affs_for(target)
        affliction_registered = False
        for i in self.AFFLICTION_MANIPULATORS:
            if i == None:
                affliction_registered = target_affs.activate(aff)
            else:
                affliction_registered = target_affs.activate(aff.replace(i[0], i[1]))

            if affliction_registered:
                break

        if not affliction_registered:
            self.mud.warn("No affliction '%s' found" % aff)

        self.__print_target_affs(target, effect)

    def __print_target_affs(self, target, effect=""):
        affs = self.__get_affs_for(target)
        self.mud.echop("@{Cgreen}%s afflictions @{Cwhite}(%s)@{Cgreen}: [@{Cred} %s @{Cgreen}]@{n}" % (target.title(), effect, ", ".join(affs.get_active())))

    def clear_target_affs(self):
        self.target_afflictions = {}

    def venom_afflict(self, venom):
        if self.ignore_next_venom:
            self.ignore_next_venom = False
            self.rebounding_ignore_guard.reset()
            return

        target = self.state["combat"]["target"]
        t_affs = self.__get_affs_for(target).get_active()

        effect = "Venom: %s" % venom
        
        if venom == "epteth":
            if "left_arm_broken" in t_affs:
                self.__register_aff("right_arm_broken", target, effect)
            else:
                self.__register_aff("left_arm_broken", target, effect)
        elif venom == "epseth":
            if "left_leg_broken" in t_affs:
                self.__register_aff("right_leg_broken", target, effect)
            else:
                self.__register_aff("left_leg_broken", target, effect)
        elif venom == "aconite":
            self.__register_aff("stupidity", target, effect)
        elif venom == "xentio":
            self.__register_aff("confusion", target, effect)
        elif venom == "kalmia":
            self.__register_aff("asthma", target, effect)
        elif venom == "gecko":
            self.__register_aff("slickness", target, effect)
        elif venom == "slike":
            self.__register_aff("anorexia", target, effect)
        elif venom == "curare":
            self.__register_aff("paresis", target, effect)
        else:
            self.mud.warn("Unknown venom: %s" % venom)

    def parse_prompt(self, line):
        target = self.state["combat"]["target"]
        if target in self.target_afflictions:
            affs = self.target_afflictions[target]
            self.state["combat"]["target_affs"] = affs.get_active()
            self.mud.eval("/set target_affs=%s" % " ".join(affs.get_active()))
        else:
            self.state["combat"]["target_affs"] = []
            self.mud.eval("/set target_affs=")
