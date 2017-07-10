import imp

"""
Misc aliases for gameplay
"""

ALIAS_LIST = {
        # Script handling
        "reload": "/python_call main.reinstall",

        # Mounts
        "mnt": ["recall mount","qmount 18597"],
        "dis": "qdmount",
        "wolf": "recall 18597",
        "returnm": "return mount duiranstable",

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
        }

def install(builder):
    builder.build(ALIAS_LIST)
