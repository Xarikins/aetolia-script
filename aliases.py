"""
Misc aliases for gameplay
"""

ALIAS_LIST = {
        # Script handling
        "reload": "/python_call main.reinstall",

        # Emotes
        "hb *": "/send heartbeat %2",
        "hb": "/send heartbeat",

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
        "wi *": "/send web invite %2",
        "wa": "/send web accept",
        "wq": "/send web quit",
        "su": "survey",
        "setup tent": "outc 3 cloth;outc 3 rope;outc 3 wood;tent setup",
        "campfire": "outc 3 wood;campfire build;incall",
        "stoke": "outc 1 wood;campfire stoke;incall",
        "cs *": "/send clan switch %2",
        "letter": "/send get letter from satchel",

        # Item handling
        "pu": ";".join([
            "outc reishi",
            "outc yarrow",
            "outc willow",
            "put reishi in pipe139519",
            "put yarrow in pipe144662",
            "put willow in pipe147400",
            "incall"
            ]),

        # Herbalism
        "paste *": "prepare %2 paste",
        "anabiotic *": "prepare %2 anabiotic",

        # Refining
        "shall": ["icon", "icon whirl"],
        "shackle *": "qe refining shackle %2",
        "hand in mist": [ "remove gauntlet293814", "give gauntlet293814 to barakin", "qeb wear gauntlet293814"],

        # Woodlore
        "nightingale": "qeb summon nightingale",
        "raloth": "qeb summon raloth",
        "cockatrice": "qeb summon cockatrice",
        "raven": "qeb summon raven",
        "animals": [
                "summon badger",
                "q summon raven",
                "q summon bear",
                "q summon crocodile",
                "q camo",
                ],
        "camo": "qeb camouflage",
        "track *": ["dis", "qmount bear", "/send track %2"],

        # Shopping
        "buy cask*": "buy refill from %2 into fluidcache",
        "refill *": "buy refill from %2 into fluidcache",

        # Emotes
        "pants *": "/send emote suddenly sneaks up behind \\$\%2 and in a rapid motion pulls down \\$\%2_\%3 pants for all to see"
        }

REG_ALIAS_LIST = {
        "^(sell .*)$": "generosity;qeb %P1",
        "^(give .*)$": "generosity;qeb %P1",
        "^(put .*)$": "generosity;qeb %P1",
        "^(drop .*)$": "generosity;qeb %P1",
        "^ooc (\w+) (.+)$": "/send tell %P1 ((ooc: %P2 ))",
        }

def install(builder, mud):
    builder.build(ALIAS_LIST)
    builder.build(REG_ALIAS_LIST, "regexp")
    mud.eval("/def key_tab = /complete")
