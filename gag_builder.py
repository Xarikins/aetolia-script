from macro_builder import MacroBuilder

class GagBuilder(MacroBuilder):

    def build(self, macros, mType = "regexp"):
        definition = "/def -p1 -ag -m%s -t'%s' = %s"
        super(GagBuilder, self)._build(definition, macros, mType)

