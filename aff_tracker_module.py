from core.module import Module
from core.prompt_listener import PromptListener
from affliction_container import AfflictionContainer

class AffTrackerModule(Module, PromptListener):

    AFFLICTION_MANIPULATORS = [
            None,
            (" ", ""),
            (" ", "-"),
            (" ", "_")
            ]

    def __init__(self, *args):
        super(AffTrackerModule, self).__init__(*args)
        self.target_afflictions = {}
        
        self.state["alias_builder"].build({
            "tclear": self.clear_target_affs,
            })

        self.state["trigger_builder"].build({
            "^You discern that (\w+) has cured the effects of (.+)\.$": {
                "fun": self.__clear_aff,
                "arg": "'%P2' '%P1'",
                },
            "^(\w+) presses a (\w+) poultice against \w+ (.+), rubbing the poultice into \w+ flesh\.$": {
                "fun": self.__register_poultice,
                "arg": "'%P2' '%P1' '%P3'",
                },
            "^(\w+) takes a long drag off \w+ pipe filled with (\w+)\.$": {
                "fun": self.__register_smoke,
                "arg": "'%P2' '%P1'",
                },
            "^(\w+) swallows a (\w+) pill\.$": {
                "fun": self.__register_pill,
                "arg": "'%P2' '%P1'",
                },
            "^Your \w+ has afflicted (\w+) with (.+)\.$": \
                self.__trigger_definition("'%P2' '%P1'"),
            "^(\w+) suddenly seizes up, \w+ entire body locked by paralysis\.$": \
                self.__trigger_definition("paralysis '%P1'"),
            })

    def __trigger_definition(self, args):
        return {
                "fun": self.__register_aff,
                "arg": args,
                }

    def __get_affs_for(self, target):
        target = target.lower()
        if target in self.target_afflictions:
            return self.target_afflictions[target]
        return None

    def __register_pill(self, pill, target):
        affs = self.__get_affs_for(target)
        if affs and affs.get_pill():
            for a in affs.get_pill().values():
                if a["pill"] == pill:
                    affs.__deactivate(a["name"])
                    return

    def __register_poultice(self, poultice, target, limb = ""):
        affs = self.__get_affs_for(target)
        if limb == skin:
            limb = ""
        if affs and affs.get_poultice():
            for a in affs.get_poultice().values():
                if a["poultice"] == poultice and a["body_part"] == limb:
                    affs.__deactivate(a["name"])
                    return

    def __register_smoke(self, herb, target):
        affs = self.__get_affs_for(target)
        if affs and affs.get_smoke():
            for a in affs.get_poultice().values():
                if a["smoke"] == smoke:
                    affs.__deactivate(a["name"])
                    return

    def __clear_aff(self, aff, target):
        target_affs = self.__get_affs_for(target)
        affliction_deregistered = False
        for i in self.AFFLICTION_MANIPULATORS:
            if i == None:
                affliction_deregistered = target_affs.__deactivate(aff)
            else:
                affliction_deregistered = target_affs.__deactivate(aff.replace(i[0], i[1]))

            if affliction_deregistered:
                break

    def __register_aff(self, aff, target = ""):
        if not target:
            target = self.state["combat"]["target"]
        target = target.lower()

        if not target in self.target_afflictions:
            target_afflictions[target] = AfflictionContainer()

        target_affs = self.target_afflictions[target]
        affliction_registered = False
        for i in self.AFFLICTION_MANIPULATORS:
            if i == None:
                affliction_registered = target_affs.__activate(aff)
            else:
                affliction_registered = target_affs.__activate(aff.replace(i[0], i[1]))

            if affliction_registered:
                break

        if not affliction_registered:
            self.mud.warn("No affliction '%s' found" % aff)

    def clear_target_affs(self):
        self.target_afflictions = {}

    def parse_prompt(self, line):
        target = self.state["combat"]["target"]
        if target in self.target_afflictions:
            affs = self.target_afflictions[target]
            self.mud.eval("/set target_affs=%s" % " ".join(affs.get_active()))
