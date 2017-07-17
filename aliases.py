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
        "go not": ["clo", "ms", "path track not"],
        "go duiran": ["clo", "ms", "path track duiran"],
        "go enorian": ["clo", "ms", "path track enorian"],
        "go esterport": ["clo", "ms", "path track esterport"],
        "go tear": ["clo", "path track lleistear"],
        "go": ["ms", "path go gallop"],
        "go *": ["ms", "/send say duanathar;path track %2"],
        "pt *": "/send path track %2",
        "pf *": "/send path find %2",

        # Misc
        "sc": "sacrifice corpses",
        "lip": "look in pack",
        "gg *": "get %2 gold from pack",
        "pgip": "/send put gold in pack",
        "part": "point ring51192 at ground",
        "part *": "point ring51192 %2",
        "quit": [
            "incall",
            "ms",
            "dis",
            "returnm",
            "pgip",
            "/send quit"
            ],
        "fs *": "farsee %2",
        "en *": "enemy %2",
        "unen *": "unenemy %2",
        "wi *": "web invite %2",
        "wa": "web accept",
        "wq": "web quit",
        "su": "survey",
        "setup tent": "outc 3 cloth;outc 3 rope;outc 3 wood;tent setup",
        "campfire": "outc 3 wood;campfire build;incall",
        "stoke": "outc 1 wood;campfire stoke;incall",
        "cs *": "/send clan switch %2",

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
        "paste *": "outc %2 berberis;outc %2 yarrow;prepare %2 paste",
        "anabiotic *": "outc %2 birthwort;outc %2 yarrow;outc %2 madder;prepare %2 anabiotic",

        # Summoning
        "nightingale": "qeb summon nightingale",
        "raloth": "qeb summon raloth",
        "cockatrice": "qeb summon cockatrice",
        "raven": "qeb summon raven",
        }

REG_ALIAS_LIST = {
        "^(sell .*)$": "generosity;qeb %P1",
        "^(give .*)$": "generosity;qeb %P1",
        "^(put .*)$": "generosity;qeb %P1",
        "^h (.+)$": "harvest all %P1",
        "^ooc (\w+) (.+)$": "/send tell %P1 ((ooc: %P2 ))",
        }

def install(builder, mud):
    builder.build(ALIAS_LIST)
    builder.build(REG_ALIAS_LIST, "regexp")
    mud.eval("/def key_tab = /complete")
