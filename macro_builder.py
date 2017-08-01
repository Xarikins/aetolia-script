class MacroBuilder():

    def __init__(self, mud, cb_handler):
        self.mud = mud
        self.cb_handler = cb_handler

    def _build(self, definition, macros, **kwargs):
        for trig, cmd in macros.items():
            self.__register_macro(definition, trig, cmd, **kwargs)

    def __register_macro(self, definition, trig, cmd, **kwargs):
        trig = self.__escape_trigger(trig)
        prio = kwargs.get("prio", 1)
        mType = kwargs.get("mType", "glob")
        command = ""

        if type(cmd) == list:
            command = "\%;".join(list(map(self.__escape_command, cmd)))
        elif type(cmd) == dict:
            command = self.__command_from_dict(cmd)
        elif callable(cmd):
            command = self.__command_from_cmd(cmd)
        else:
            command = self.__escape_command(cmd)

        self.mud.eval(definition % (prio, mType, trig, command))

    def __escape_trigger(self, trig):
        trig = trig.replace("$", "\$")
        trig = trig.replace("\w", "\\\\w")
        trig = trig.replace("\d", "\\\\d")
        trig = trig.replace("\.", "\\\\.")
        trig = trig.replace("\(", "\\\\(")
        trig = trig.replace("\)", "\\\\)")
        trig = trig.replace("\:", "\\\\:")
        trig = trig.replace("\[", "\\\\[")
        trig = trig.replace("\]", "\\\\]")
        trig = trig.replace("'", "\\\\'")
        trig = trig.replace(",", "\\\\,")
        return trig

    def __escape_command(self, cmd):
        cmd = cmd.replace("%", "\%")
        return cmd

    def __command_from_dict(self, cmd):
        command = self.__command_from_cmd(cmd["fun"])
        if "arg" in cmd:
            command += " " + cmd["arg"].replace("%", "\\%")
        return command

    def __command_from_cmd(self, cmd):
        self.cb_handler.registerCallback(cmd)
        return "/python_call main.cb %s" % cmd.__name__
