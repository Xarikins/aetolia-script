from core.module import Module
from collections import deque

class HarvestModule(Module):

    def __init__(self, *args):
        super(HarvestModule, self).__init__(*args)
        
        self.last_harvest = ""
        self.harvest_directions = deque([])

        self.state["alias_builder"].build({
            "h": self.harvest,
            "hs": "harvest stop",
            "ham": "harvest amount",
            "hdc": self.clear_harvest_directions,
            "hd *": {
                "fun": self.add_harvest_direction,
                "arg": "'%2'",
                }
            })

        self.state["alias_builder"].build({
            "^h (.+)$": {
                "fun": self.harvest,
                "arg": "'%P1'",
                }
            }, "regexp")

        self.state["trigger_builder"].build({
            "^There is nothing left here to harvest\.$": self.pop_harvest_direction,
            })

        self.state["gag_builder"].build({
            "^You have harvested (\d+) of (\d+) herbs this week\.$": {
                "fun": self.harvest_amount_disp,
                "arg": "'%P1' '%P2'",
                },
            })

    def harvest_amount_disp(self, current, limit):
        self.mud.info("Harvested: %s / %s" % (current, limit))

    def harvest(self, cmd = ""):
        if not self.last_harvest and not cmd:
            self.mud.warn("No harvest command")
            return

        if cmd:
            self.last_harvest = cmd

        self.mud.send("harvest all %s" % self.last_harvest)

    def clear_harvest_directions(self):
        seld.harvest_directions = deque([])

    def add_harvest_direction(self, direction):
        self.mud.info("Adding harvest direction: %s" % direction)
        self.harvest_directions.append(direction)

    def pop_harvest_direction(self):
        if self.harvest_directions:
            direction = self.harvest_directions.popleft()
            self.mud.info("Popping harvest direction: %s" % direction)
            self.mud.send(direction)
            self.harvest()
