import tf
import imp
import alias_builder

ALIAS_LIST = {
        # Script handling
        "reload": "/python_call main.reinstall",
        "debug": "/python_call main.toggle_debug",

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

def install():
    imp.reload(alias_builder)
    alias_builder.build_aliases(ALIAS_LIST)

install()
    
