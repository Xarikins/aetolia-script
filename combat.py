import tf
import imp
import alias_builder
import globals

ALIASES_REG = {
        # Target alias
        "^x ([\\\w\\\d]+)\\$": "/python_call combat.target \\%2",
        }
ALIASES_GLOB = {
        # Bashing aliases
        "at": "/python_call combat.at",
        }

def at(arg):
    tf.eval("/send dhuriv combo %s slash stab" % globals.combat["target"])

def target(target):
    globals.combat["target"] = target
    print("Current target: %s" % globals.combat["target"])

def _install():
    imp.reload(alias_builder)
    alias_builder.build_aliases(ALIASES_REG, "regexp")
    alias_builder.build_aliases(ALIASES_GLOB)

_install()
