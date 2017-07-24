from macro_builder import MacroBuilder

class AliasBuilder(MacroBuilder):

    def build(self, macros, mType = "glob"):
        definition = "/def -waetolia -p1 -m%s -h'SEND %s' = %s"
        super(AliasBuilder, self)._build(definition, macros, mType)
