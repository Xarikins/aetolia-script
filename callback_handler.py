class CallbackHandler():

    def __init__(self):
        self.callbacks = {}

    def registerCallback(self, function):
        name = function.__name__
        if name in self.callbacks:
            raise ValueError("Duplicate callback function named: %s" % name)
        self.callbacks[name] = function

    def triggerCallback(self, name, arguments):
        if not name in self.callbacks:
            return
        else:
            self.callbacks[name](*arguments)
