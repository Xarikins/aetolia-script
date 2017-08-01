from macro_builder import MacroBuilder

class GagBuilder(MacroBuilder):

    def build(self, macros, mType = "regexp", **kwargs):
        kwargs["mType"] = mType
        definition = "/def -waetolia -p%d -ag -m%s -t'%s' = %s"
        super(GagBuilder, self)._build(definition, macros, **kwargs)

