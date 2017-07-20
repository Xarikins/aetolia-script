import os
import json
from collections import deque

class Path():

    def __init__(self, mud):
        self.mud = mud
        self.path = deque([])

    def load(self, name):
        filename = "/home/linus/muds/aetolia/paths/%s.json" % name
        if not os.path.isfile(filename):
            self.mud.warn("File: %s doesn't exist" % filename)
            return

        path = None
        with open(filename, "r") as f:
            path = json.loads(f.read())

        self.path = deque(path)

        self.mud.info("Path %s loaded" % name)

    def has_step(self):
        return self.length() > 0

    def get_next(self):
        step = self.path.popleft()
        return step

    def length(self):
        return len(self.path)

    def clear(self):
        self.mud.info("Clearing path")
        self.path = deque([])
