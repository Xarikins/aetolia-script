import shlex

class CallbackHandler():

    def __init__(self):
        self.callbacks = {}
        self.sources = {}
        self.gmcp_callbacks = {}

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

    def registerGmcpCallback(self, key, function):
        if key not in self.gmcp_callbacks:
            self.gmcp_callbacks[key] = []
        self.gmcp_callbacks[key].append(function)

    def triggerGmcpCallback(self, key, body):
        if key not in self.gmcp_callbacks:
            return
        for fun in self.gmcp_callbacks[key]:
            fun(body)

