from collections import deque

class CommandQueue():
        
    def __init__(self, player):
        self.queue = deque([])
        self.player = player
        self.ready = False

    def trigger(self):
        if not len(self.queue):
            return None

        ba = self.player["balance"]
        eq = self.player["equilibrium"]

        if not ba or not eq:
            self.ready = True
            return None

        if ba and eq and self.ready:
            self.ready = False
            return self.queue.popleft()
        else:
            return None

    def append(self, cmd):
        self.queue.append(cmd)

    def clear(self):
        self.queue.clear()
