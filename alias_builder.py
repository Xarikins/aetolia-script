from macro_builder import MacroBuilder

class AliasBuilder(MacroBuilder):

    def build(self, macros, mType = "glob", **kwargs):
        kwargs["mType"] = mType
        definition = "/def -waetolia -p%d -m%s -h'SEND %s' = %s"
        super(AliasBuilder, self)._build(definition, macros, **kwargs)
