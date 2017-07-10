class CallbackHandler():

    def __init__(self):
        self.callbacks = {}

    def registerCallback(self, name, function):
        self.callbacks[name] = function

    def triggerCallback(self, name, arguments):
        if not self.callbacks[name]:
            return
        else:
            self.callbacks[name](*arguments)
