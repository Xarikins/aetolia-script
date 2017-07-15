from macro_builder import MacroBuilder

class TriggerBuilder(MacroBuilder):

    def build(self, macros, mType = "regexp"):
        definition = "/def -p1 -m%s -t'%s' = %s"
        super(TriggerBuilder, self)._build(definition, macros, mType)

