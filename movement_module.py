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
            "in": walk_definition,
            "out": walk_definition,
            "u": walk_definition,
            "d": walk_definition,

            "ee": self.__gallop_definition_for("e"),
            "nee": self.__gallop_definition_for("ne"),
            "see": self.__gallop_definition_for("se"),
            "ww": self.__gallop_definition_for("w"),
            "nww": self.__gallop_definition_for("nw"),
            "sww": self.__gallop_definition_for("sw"),
            "nn": self.__gallop_definition_for("n"),
            "ss": self.__gallop_definition_for("s"),
            "dd": self.__gallop_definition_for("d"),
            "uu": self.__gallop_definition_for("u"),

            "clo": "/send say duanathar",
            "cu": "/send climb up",
            "cd": "/send climb down",

            "fo *": "/send follow %2",

            # Pathing
            "go tear": ["clo", "/send path find lleistear;path go gallop"],
            "go ollin": ["clo", "/send path find 19521;path go gallop"],
            "go fracture": ["clo", "/send path find 10046;path go gallop"],
            "go": ["ms", "/send path go gallop"],
            "go *": ["ms", "/send say duanathar;path find %2;path go gallop"],
            "pt *": "/send path track %2",
            "pf *": "/send path find %2",

            # Rescue
            "revive *": ["go %2", "mq get body;say duanathar;scent", "q path find lleistear;path go gallop", "mq bathe body"],

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

    def __gallop_definition_for(self, direction):
        return {
                "fun": self.__gallop,
                "arg": direction,
                }

    def __gallop(self, direction):
        if not self.state["player"]["mounted"]:
            self.mud.eval("ms")
        self.mud.send("gallop %s" % direction)

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
        filename = "%s/%s.json" % (self.state["settings"]["paths"]["path_dir"], name)
        self.mud.info("Writing file: %s" % filename)
        with open(filename, "w") as f:
            f.write(json.dumps(self.recorded_path))
        self.recording = False
        self.recoreded_path = []
