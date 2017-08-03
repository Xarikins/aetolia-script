"""
Misc aliases for gameplay
"""

ALIAS_LIST = {
        # Script handling
        "reload": "/python_call main.reinstall",

        # Weapons
        "dhurive": ["unwield sickle", "wield dhurive"],
        "sickle": ["secure weapon", "wield sickle"],

        # Emotes
        "hb *": "/send heartbeat %2",

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
        "wi *": "web invite %2",
        "wa": "web accept",
        "wq": "web quit",
        "su": "survey",
        "setup tent": "outc 3 cloth;outc 3 rope;outc 3 wood;tent setup",
        "campfire": "outc 3 wood;campfire build;incall",
        "stoke": "outc 1 wood;campfire stoke;incall",
        "cs *": "/send clan switch %2",

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
        "deathsight": ["outc thanatonin", "eat thanatonin"],

        # Herbalism
        "paste *": "prepare %2 paste",
        "anabiotic *": "prepare %2 anabiotic",

        # Refining
        "shackle *": "qe refining shackle %2",

        # Summoning
        "nightingale": "qeb summon nightingale",
        "raloth": "qeb summon raloth",
        "cockatrice": "qeb summon cockatrice",
        "raven": "qeb summon raven",
        "animals": [
                "q summon nightingale",
                "q summon raven",
                "q summon raloth",
                "q summon crocodile",
                "q camo",
                ],
        "camo": "qeb camouflage",

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
