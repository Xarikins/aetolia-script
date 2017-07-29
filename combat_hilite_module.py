from core.module import Module

class CombatHiliteModule(Module):

    def __init__(self, *args):
        super(CombatHiliteModule, self).__init__(*args)

        self.state["gag_builder"].build({
            "^(\w+) parries the attack on \w+ (.+) with a deft maneuver\.$": self.__warn_definition("%P1 'parried %P2'"),
            "^(\w+) has been slain by (\w+)\.$": self.__info_definition("'%P2 killed %P1'"),
            "^The attack rebounds back onto you!$": self.__warn_definition("Rebounding"),
            "^You begin to follow (\w+)\.$": self.__info_definition("'Following %P1'"),
            "^Your arrow strikes true\.$": self.__info_definition("'Arrow hit'"),
            "^(\w+) has writhed free of \w+ bindings\.$": self.__info_definition("'%P1 writhed free'"),
            "^You suddenly perceive the vague outline of an aura of rebounding around (\w+)\.$": \
                    self.__warn_definition("'Rebounding around %P1'"),
            "^The bone marrow coating (\w+)'s body sloughs off from \w+ skin\.$": \
                    self.__info_definition("'%P1 lost fangbarrier'"),
            "^(\w+)'s aura of weapons rebounding disappears\.$": \
                    self.__info_definition("'%P1 lost rebounding'"),
            })

    def __warn_definition(self, args):
        return {
                "fun": self.warn,
                "arg": args,
                }

    def __info_definition(self, args):
        return {
                "fun": self.info,
                "arg": args,
                }

    def __panic_definition(self, args):
        return {
                "fun": self.panic,
                "arg": args,
                }

    def warn(self, *args):
        self.mud.warn(" ".join(args))
 
    def panic(self, *args):
        self.mud.panic(" ".join(args))
 
    def info(self, *args):
        self.mud.info(" ".join(args))
