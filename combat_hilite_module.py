from core.module import Module

class CombatHiliteModule(Module):

    def __init__(self, *args):
        super(CombatHiliteModule, self).__init__(*args)

        self.state["gag_builder"].build({
            "^(\w+) parries the attack on \w+ (.+) with a deft maneuver\.$": self.__warn_definition("%P1 'parried %P2'"),
            "^(\w+) has been slain by (\w+)\.$": self.__info_definition("'%P2 killed %P1'"),
            "^You begin to follow (\w+)\.$": self.__info_definition("'Following %P1'"),
            "^Your arrow strikes true\.$": self.__info_definition("'Arrow hit'"),
            "^(\w+) has writhed free of \w+ bindings\.$": self.__info_definition("'%P1 writhed free'"),
            "^The bone marrow coating (\w+)'s body sloughs off from \w+ skin\.$": \
                    self.__info_definition("'%P1 lost fangbarrier'"),
            "^You recognize the song as a signal from a Sentinel\:$": \
                    self.__info_definition("'Sentinel signal:'"),
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
