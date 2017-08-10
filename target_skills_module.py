from core.module import Module

class TargetSkillsModule(Module):

    def __init__(self, *args):
        super(TargetSkillsModule, self).__init__(*args)

        self.register("tp", "qeb touch prism")
        self.register("braz", "qeb touch brazier")
        self.register("web", "qeb touch web")
        self.register("ten", "qeb touch tentacle")

        self.register("comb", "qeb resin combust")
        self.register("lp", "qeb dhuriv pierce <target> left")
        self.register("rp", "qeb dhuriv pierce <target> right")
        self.register("ls", "qeb dhuriv sever <target> left")
        self.register("rs", "qeb dhuriv sever <target> right")
        
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

        if "<target>" in skill:
            skill = skill.replace("<target>", target)
        else:
            skill += " %s" % target

        self.mud.send(skill)
