from core.module import Module

class TargetSkillsModule(Module):

    def __init__(self, *args):
        super(TargetSkillsModule, self).__init__(*args)

        self.register("tp", "touch prism")
        self.register("braz", "touch brazier")
        self.register("web", "touch web")
        self.register("ten", "touch tentacle")
        
    def register(self, alias, skill):
        data = {}

        data[alias] = {
                "fun": self.target_callback,
                "arg": "'%s'" % skill,
                }

        data["%s *" % alias] = {
                "fun": self.target_callback,
                "arg": "'%s' '%%2'" % skill,
                }

        self.state["alias_builder"].build(data)

    def target_callback(self, skill, target=""):
        if not target:
            target = self.state["combat"]["target"]

        self.mud.send("%s %s" % (skill, target))
