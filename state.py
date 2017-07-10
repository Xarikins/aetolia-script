from imp import reload
from communicator import Communicator
from alias_builder import AliasBuilder
from trigger_builder import TriggerBuilder
from cmd_queue import CommandQueue
from callback_handler import CallbackHandler

def new():
    mud = Communicator()
    callback_handler = CallbackHandler()
    alias_builder = AliasBuilder(mud, callback_handler)
    trigger_builder = TriggerBuilder(mud, callback_handler)

    player = {
            "balance": True,
            "lbalance": True,
            "rbalance": True,
            "equilibrium": True,
            "health": 0,
            "mana": 0,
            "prone": False,
            "deaf": True,
            "blind": True,
            "fangbarrier": True,
            }

    return {
            "combat": {
                "target": "",
                },
            "player": player,
            "mode": {
                "bashing": False,
                },
            "communicator": mud,
            "alias_builder": alias_builder,
            "trigger_builder": trigger_builder,
            "cmd_queue": CommandQueue(player),
            "callback_handler": callback_handler,
            }
