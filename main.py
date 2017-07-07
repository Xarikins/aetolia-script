import tf
import sys
import imp

import globals
import info_here_parser

MACRO_LINE = "py_line"
MODULES = [
        "aliases",
        "combat"
        ]

GLOBAL = {
        "target": "",
        }

# Setup print to print to tf
sys.stdout.output = tf.out

# Variables
debug = False

def reinstall(arg):
    tf.eval("***REMOVED***")

def toggle_debug(arg):
    global debug
    debug = not debug
    if debug:
        print("Debug mode on")
    else:
        print("Debug mode off")

def handle_line(line):
    if debug:
        print("Received line: %s" % line)
    info_here_parser.parse_line(line)

def _load_module(module):
    print("---> %s" % module)
    tf.eval("/python_load %s" % module)

def _install():
    # Reload modules
    imp.reload(info_here_parser)

    # Purge all macros
    print("Purging existing macros...")
    tf.eval("/purge")
    print("...DONE")
    print("")

    print("Loading modules...")
    for mod in MODULES:
        _load_module(mod)
    print("")

    print("Installing line listener...")
    tf.eval("/def -p9 -F -q -mregexp -t'^.*\\$' = /python_call main.handle_line \\%*")
    print("...DONE")
    print("")

    print("Python 'main' loaded")

_install()
globals.init()
