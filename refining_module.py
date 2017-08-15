from core.module import Module
from collections import deque

class RefiningModule(Module):

    def __init__(self, *args):
        super(RefiningModule, self).__init__(*args)

        self.room_queue = deque([])
        self.foci_located = False
        self.searching = False
        self.last_room = 0
        
        foci_definition = {
                "fun": self.foci_trigger,
                "arg": "%P1",
                }

        self.state["trigger_builder"].build({
            "^You detect (\d+) (lesser|minor) (foci|focus).$": foci_definition,
            "^There are a total of \d+ foci globally\.$": self.complete_check,
            "^You have moved away from your path\.$": self.path_fail,
            })

        self.state["alias_builder"].build({
            "startfindfoci": self.start,
            "findfoci": self.find_foci,
            "resumefoci": self.resume,
            "stopfoci": self.stop,
            })

    def foci_trigger(self, num):
        count = int(num)
        if count > 0:
            self.foci_located = True

    def complete_check(self):
        if self.foci_located:
            self.mud.info("FOCI")
            self.foci_located = False
        else:
            self.find_foci()

    def start(self):
        self.mud.info("Starting FOCI search")
        self.searching = True
        self.load_path_rooms()
        self.find_foci()

    def stop(self):
        self.mud.info("Stopping FOCI search")
        self.searching = False

    def resume(self):
        self.mud.info("Resuming FOCI search")
        self.searching = True
        self.find_foci()

    def find_foci(self):
        if not self.room_queue or not self.searching:
            return

        self.last_room = self.room_queue.popleft()
        self.mud.info("Tracking to %d (%d)" % (self.last_room, len(self.room_queue)))
        self.mud.eval("mq leylines")
        self.mud.eval("q go %d" % self.last_room)

    def path_fail(self):
        if self.last_room:
            self.mud.info("Pathing failed, retrying")
            self.mud.send("path track %d" % self.last_room)

    def load_path_rooms(self):
        self.mud.info("Loading rooms to queue")
        rooms = [
                250, 36824, 20389, 5599, 22477, 22824, 10813, 26690,
                16437, 18462, 20754, 5682, 21908, 3106, 1745, 12332,
                20450, 24628, 22702, 23128, 1773, 16706, 17612, 20932,
                19323, 58675, 3887, 55189, 19621, 17032, 18082, 25408,
                27704, 13425, 20281, 56942, 54482, 4740, 19320, 20855,
                23202, 56647, 23791, 19810, 26820, 55276, 19344, 19602,
                22866, 57334, 19854, 4828, 60845, 19626, 22226, 10046,
                15714, 3273, 15344, 26920, 14729, 19987, 59609, 2030,
                16282, 4964, 35217, 56731, 36270, 36677, 38090, 38894,
                16274, 45483, 49286, 36824, 57521, 54770
                ]

        rooms.sort()

        self.room_queue = deque(rooms)
