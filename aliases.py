"""
Misc aliases for gameplay
"""

ALIAS_LIST = {
        # Script handling
        "reload": "/python_call main.reinstall",

        # Mounts
        "ms": ["recall mount","qmount 18597"],
        "dis": "qdmount",
        "wolf": "recall 18597",
        "returnm": "return mount duiranstable",

        # Weapons
        "dhurive": ["unwield sickle", "wield dhurive"],
        "sickle": ["secure weapon", "wield sickle"],

        # Movement
        "ee": "gallop e",
        "nee": "gallop ne",
        "see": "gallop se",
        "ww": "gallop w",
        "nww": "gallop nw",
        "sww": "gallop sw",
        "nn": "gallop n",
        "ss": "gallop s",
        "dd": "gallop d",
        "uu": "gallop u",
        "clo": "say duanathar",
        "cu": "climb up",
        "cd": "climb down",

        # Pathing
        "go not": ["clo", "path find not", "ms", "path go gallop"],
        "go duiran": ["clo", "path find duiran", "ms", "path go gallop"],
        "go enorian": ["clo", "path find enorian", "ms", "path go gallop"],
        "go esterport": ["clo", "path find esterport", "ms", "path go gallop"],
        "go tear": ["clo", "path find lleistear", "ms", "path go gallop"],
        "go": ["ms", "path go gallop"],
        "go *": ["ms", "/send say duanathar;path find \%2;path go gallop"],

        # Misc
        "sc": "sacrifice corpses",
        "lip": "look in pack",
        "gg *": "get \%2 gold from pack",
        "pgip": "put gold in pack",
        "part": "point ring51192 at ground",
        "part *": "point ring51192 \%2",
        "quit": [
            "incall",
            "ms",
            "dis",
            "returnm",
            "pgip",
            "/send quit"
            ],

        # Item handling
        "pipeup": ";".join([
            "outc reishi",
            "outc yarrow",
            "outc willow",
            "put reishi in pipe139519",
            "put yarrow in pipe144662",
            "put willow in pipe147400",
            "incall"
            ]),
        "deathsight": ["outc thanatonin", "eat thanatonin"],

        # Herbalism
        "paste *": "outc \%2 berberis;outc \%2 yarrow;prepare \%2 paste",
        "anabiotic *": "outc \%2 birthwort;outc \%2 yarrow;outc \%2 madder;prepare \%2 anabiotic",
        }

REG_ALIAS_LIST = {
        "^(sell .*)\$": "generosity;qeb \%P1",
        "^(give .*)\$": "generosity;qeb \%P1",
        "^h (.+)\$": "harvest all \%P1",
        }

def install(builder):
    builder.build(ALIAS_LIST)
    builder.build(REG_ALIAS_LIST, "regexp")
