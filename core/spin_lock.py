from threading import Timer

class SpinLock():

    def __init__(self):
        self.lock = True

    def delay(self, time, func):
        Timer(time, self.__reset).start()
        while self.lock:
            continue
        func()

    def __reset(self):
        self.lock = False
