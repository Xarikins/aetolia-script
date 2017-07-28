from imp import reload
from collections import deque
import communicator
import alias_builder
import trigger_builder
import gag_builder
import callback_handler

def new():
    reload(communicator)
    reload(callback_handler)
    reload(alias_builder)
    reload(trigger_builder)
    reload(gag_builder)

    mud = communicator.Communicator()
    cb_handler = callback_handler.CallbackHandler()
    a_builder = alias_builder.AliasBuilder(mud, cb_handler)
    t_builder = trigger_builder.TriggerBuilder(mud, cb_handler)
    g_builder = gag_builder.GagBuilder(mud, cb_handler)

    player = {
            "balance": True,
            "lbalance": True,
            "rbalance": True,
            "equilibrium": True,
            "health": 0,
            "mana": 0,
            "prone": False,
            "writhing": False,
            "mounted": False,
            "deaf": True,
            "blind": True,
            "cloaked": True,
            "fangbarrier": True,
            "affs": [],
            "missing_defs": [],
            }

    return {
            "combat": {
                "target": "",
                },
            "player": player,
            "mode": {
                "bashing": False,
                "fight": False,
                },
            "gmcp": {},
            "communicator": mud,
            "alias_builder": a_builder,
            "trigger_builder": t_builder,
            "gag_builder": g_builder,
            "callback_handler": cb_handler,
            "cmd_queue": deque([]),
            }
