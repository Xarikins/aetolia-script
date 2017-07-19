from threading import Timer

class SpamGuard():

    def __init__(self, time):
        self.__locked = False
        self.time = time
        self.timer = None

    def reset(self):
        if self.timer:
            self.timer.cancel()
        self.__locked = False

    def lock(self):
        if not self.__locked:
            self.__locked = True
            self.timer = Timer(self.time, self.reset)
            self.timer.start()
            return True
        else:
            return False

    def locked(self):
        return self.__locked
