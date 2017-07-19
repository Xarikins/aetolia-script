from threading import Timer

class SpecialCure():

    def __init__(self, mud):
        self.spam_guards = {}
        self.mud = mud

    def use(self, command):
        if self.__spam_guarded(command):
            return
        self.__spam_guard(command)
        self.mud.send(command)
        Timer(2, self.reset_guard, [command]).start()

    def __spam_guarded(self, command):
        if command.startswith("sip"):
            return "sip" in self.spam_guards
        else:
            return command in self.spam_guards

    def __spam_guard(self, command):
        if command.startswith("sip"):
            self.spam_guards["sip"] = True
        else:
            self.spam_guards[command] = True

    def reset_guard(self, command):
        if command.startswith("sip"):
            del self.spam_guards["sip"]
        else:
            del self.spam_guards[command]

    def available(self, command):
        return command not in self.spam_guards
