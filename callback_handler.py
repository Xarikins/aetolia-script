import shlex

class CallbackHandler():

    def __init__(self):
        self.callbacks = {}
        self.sources = {}

    def registerCallback(self, function):
        name = function.__name__
        if name in self.callbacks:
            print(" -- Multiple callbacks to: %s" % name)
            return
        self.callbacks[name] = function

    def triggerCallback(self, name, arguments):
        if not name in self.callbacks:
            return
        else:
            self.callbacks[name](*arguments)
