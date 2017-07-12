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

        # Item handling
        "pipeup": [
            "outc reishi",
            "outc yarrow",
            "outc willow",
            "put reishi in pipe139519",
            "put yarrow in pipe144662",
            "put willow in pipe147400",
            ],
        "deathsight": ["outc thanatonin", "eat thanatonin"],
        }

REG_ALIAS_LIST = {
        "^(sell .*)\$": "generosity;qeb \%P1",
        "^(give .*)\$": "generosity;qeb \%P1",
        }

def install(builder):
    builder.build(ALIAS_LIST)
    builder.build(REG_ALIAS_LIST, "regexp")
