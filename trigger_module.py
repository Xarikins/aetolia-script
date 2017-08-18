from core.module import Module

class TriggerModule(Module):

    def __init__(self, *args):
        super(TriggerModule, self).__init__(*args)
        
        self.state["gag_builder"].build({
            "^Your pipe is now empty\.$": { 
                "fun": self.hilite_and_eval,
                "arg": "'warn' 'PIPE EMPTY' 'q pu'",
                }
            })

    def hilite_and_eval(self, hType, hilite, cmd):
        if hType == "warn":
            self.mud.warn(hilite)
        elif hType == "info":
            self.mud.info(hilite)
        elif hType == "panic":
            self.mud.panic(hilite)

        self.mud.eval(cmd)
