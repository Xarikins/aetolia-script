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
    try:
        args = __arg_split(arg)
        cState["callback_handler"].triggerCallback(args[0], args[1:])
        shlex_success = True
    except:
        pass

def __arg_split(arg):
    args = arg.split(" ", 1)
    if len(args) == 1:
        return args
    return [args[0]] + __arg_split_recursion(args[1])

def __arg_split_recursion(args):
    if args.startswith("'"):
        arg_list = args[1:].split("' ", 1)
        if len(arg_list) == 1:
            arg_list[0] = arg_list[0][0:-1]
            return arg_list
    else:
        arg_list = args.split(" ", 1)
        if len(arg_list) == 1:
            return arg_list

    return [arg_list[0]] + __arg_split_recursion(arg_list[1])

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
    cb("trigger_notification '(Web)' 'Serrice says, \"Target: leana's.\"'")
