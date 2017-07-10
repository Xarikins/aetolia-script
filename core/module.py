class Module():

    def __init__(self, state):
        self.state = state
        self.mud = self.state["communicator"]
