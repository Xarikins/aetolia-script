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
    # Shlex fails often. Perhaps write something better?
    try:
        args = shlex.split(arg)
        cState["callback_handler"].triggerCallback(args[0], args[1:])
    except:
        pass

def install(cState):
    print("Installing...")
    mud = cState["communicator"]

    # Clear existing
    mud.eval("/purge")

    # Install
    load_modules(cState)
    aliases.install(cState["alias_builder"], mud)

    mud.eval("/def -waetolia -p9 -F -q -mregexp -t'^.*\\$' py_line = /python_call main.handle_line \\%*")
    mud.eval("/def -waetolia -p9 -F -mregexp -q -h'PROMPT ^.*\$' prompt_trigger = /python_call main.handle_prompt \\%*")
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
    cb("trigger_notification '(Web)' 'Serrice says, \"Target: leana.\"'")
