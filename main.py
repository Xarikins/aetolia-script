import mud_wrapper as tf
import sys
import shlex
from imp import reload

import state
import aliases
import module_builder as builder

from core.prompt_listener import *
from core.line_listener import *

MACRO_LINE = "py_line"
MODULES = []

# Setup print to print to tf
sys.stdout.output = tf.out

def reinstall(arg):
    cState["communicator"].eval("***REMOVED***")

def handle_line(line):
    for mod in MODULES:
        if isinstance(mod, LineListener):
            mod.parse_line(line)

def handle_prompt(line):
    for mod in MODULES:
        if isinstance(mod, PromptListener):
            mod.parse_prompt(line)

def cb(arg):
    args = shlex.split(arg)
    cState["callback_handler"].triggerCallback(args[0], args[1:])

def install(cState):
    print("Installing...")
    mud = cState["communicator"]

    # Clear existing
    mud.eval("/purge")

    # Install
    load_modules(cState)
    aliases.install(cState["alias_builder"], mud)

    mud.eval("/def -p9 -F -q -mregexp -t'^.*\\$' py_line = /python_call main.handle_line \\%*")
    mud.eval("/def -p9 -F -mregexp -q -h'PROMPT ^.*\$' prompt_trigger = /python_call main.handle_prompt \\%*")
    print("...DONE")

    print("Python 'main' loaded")

def load_modules(cState):
    global MODULES
    MODULES = builder.build_modules(cState)

reload(state)
reload(builder)
reload(aliases)

cState = state.new()
install(cState)

if __name__ == "__main__":
    handle_line("You are afflicted with clumsiness.")
    handle_line("You have cured clumsiness.")
    handle_line("(Order): You have cured clumsiness.")
    handle_line("Your mindseye defence has been stripped.")
    handle_line("Your deathsight defence has been stripped.")
    handle_line("Your insulation defence has been stripped.")
    handle_line("Your venom_resistance defence has been stripped.")
    handle_prompt("test")
    handle_prompt("test")
    handle_prompt("test")
    handle_prompt("test")
    mud = cState["communicator"]
    mud.info("Testing info")
    mud.warn("Testing warn")
    mud.panic("Testing panic")
