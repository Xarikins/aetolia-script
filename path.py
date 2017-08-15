import os
import json
from collections import deque

class Path():

    def __init__(self, mud, path_dir):
        self.mud = mud
        self.path_dir = path_dir
        self.path = deque([])

    def load(self, name):
        filename = "%s/%s.json" % (self.path_dir, name)
        if not os.path.isfile(filename):
            self.mud.warn("File: %s doesn't exist" % filename)
            return

        path = None
        with open(filename, "r") as f:
            path = json.loads(f.read())

        self.path = deque(path)

        self.mud.info("Path %s loaded" % name)

    def has_step(self):
        return len(self.path) > 0

    def get_next(self):
        step = self.path.popleft()
        return step

    def clear(self):
        self.mud.info("Clearing path")
        self.path = deque([])

    def __len__(self):
        return len(self.path)

    def __bool__(self):
        return len(self.path)

    def __str__(self):
        return str(self.path)
