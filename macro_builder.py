class MacroBuilder():

    def __init__(self, mud):
        self.mud = mud

    def _build(self, definition, macros, mType):
        for trig, cmd in macros.items():
            self.__register_macro(definition, trig, cmd, mType)

    def __register_macro(self, definition, trig, cmd, mType = "glob"):
        command = ""

        if type(cmd) == list:
            command = "\\%;".join(cmd)
        elif type(cmd) == dict:
            command = self.__command_from_dict(cmd)
        else:
            command = cmd

        self.mud.eval(definition % (mType, trig, command))

    def __command_from_dict(self, cmd):
        command = "/python_call main.cb %s" % cmd['fun'].__name__
        if cmd["arg"]:
            command += " " + cmd["arg"]
        return command
