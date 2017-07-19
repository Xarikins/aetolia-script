from core.module import Module
import json

class MovementModule(Module):

    def __init__(self, *args):
        super(MovementModule, self).__init__(*args)
        self.recorded_path = []
        self.recording = False

        walk_definition = {
                "fun": self.__walk,
                "arg": "%1",
                }

        self.state["alias_builder"].build({

            # Movement
            "n": walk_definition,
            "e": walk_definition,
            "w": walk_definition,
            "s": walk_definition,
            "ne": walk_definition,
            "nw": walk_definition,
            "se": walk_definition,
            "sw": walk_definition,

            "ee": "/send gallop e",
            "nee": "/send gallop ne",
            "see": "/send gallop se",
            "ww": "/send gallop w",
            "nww": "/send gallop nw",
            "sww": "/send gallop sw",
            "nn": "/send gallop n",
            "ss": "/send gallop s",
            "dd": "/send gallop d",
            "uu": "/send gallop u",
            "clo": "/send say duanathar",
            "cu": "/send climb up",
            "cd": "/send climb down",

            # Pathing
            "go not": ["clo", "ms", "/send path track not"],
            "go duiran": ["clo", "ms", "/send path track duiran"],
            "go enorian": ["clo", "ms", "/send path track enorian"],
            "go esterport": ["clo", "ms", "/send path track esterport"],
            "go tear": ["clo", "/send path track lleistear"],
            "go ollin": ["clo", "/send path track 19521"],
            "go": ["ms", "/send path go gallop"],
            "go *": ["ms", "/send say duanathar;path track %2"],
            "pt *": "/send path track %2",
            "pf *": "/send path find %2",

            # Recording
            "recpath": self.toggle_recording,
            "savepath *": {
                "fun": self.save_path,
                "arg": "%2",
                },

            })

        self.state["alias_builder"].build({

            # Recording
            "^rec (.*)$": {
                "fun": self.record_action,
                "arg": "'%P1'",
                }

            }, "regexp")

    def __walk(self, direction):
        if self.recording:
            self.mud.out("Recording: %s" % direction)
            self.recorded_path.append(direction)
            self.mud.out("Path: %s" % ", ".join(self.recorded_path))
        self.mud.send(direction)

    def toggle_recording(self):
        self.recording = not self.recording
        self.mud.info("Path recording enabled" if self.recording \
                else "Path recording disabled")
        if not self.recording:
            self.recorded_path = []

    def record_action(self, action):
        self.recorded_path.append(action)
        self.mud.out("Path: %s" % ", ".join(self.recorded_path))
        self.mud.send(action)

    def save_path(self, name):
        filename = "/home/linus/muds/aetolia/paths/%s.json" % name
        self.mud.info("Writing file: %s" % filename)
        with open(filename, "w") as f:
            f.write(json.dumps(self.recorded_path))
        self.recording = False
        self.recoreded_path = []
