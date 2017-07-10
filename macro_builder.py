class MacroBuilder():

    def __init__(self, mud, cb_handler):
        self.mud = mud
        self.cb_handler = cb_handler

    def _build(self, definition, macros, mType):
        for trig, cmd in macros.items():
            self.__register_macro(definition, trig, cmd, mType)

    def __register_macro(self, definition, trig, cmd, mType = "glob"):
        command = ""

        if type(cmd) == list:
            command = "\\%;".join(cmd)
        elif type(cmd) == dict:
            command = self.__command_from_dict(cmd)
        elif callable(cmd):
            command = self.__command_from_cmd(cmd)
        else:
            command = cmd

        self.mud.eval(definition % (mType, trig, command))

    def __command_from_dict(self, cmd):
        command = self.__command_from_cmd(cmd["fun"])
        if "arg" in cmd:
            command += " " + cmd["arg"].replace("%", "\\%")
        return command

    def __command_from_cmd(self, cmd):
        self.cb_handler.registerCallback(cmd)
        return "/python_call main.cb %s" % cmd.__name__
