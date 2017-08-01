from macro_builder import MacroBuilder

class TriggerBuilder(MacroBuilder):

    def build(self, macros, mType = "regexp", **kwargs):
        kwargs["mType"] = mType
        definition = "/def -waetolia -p%d -m%s -t'%s' = %s"
        super(TriggerBuilder, self)._build(definition, macros, **kwargs)

