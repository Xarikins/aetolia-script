import tf

def build_aliases(aliases, mType = "glob"):
    for alias, cmd in aliases.items():
        _register_alias(alias, cmd, mType)

def _register_alias(alias, cmd, mType = "glob"):
    definition = "/def -p1 -m%s -h'SEND %s' = %s"
    command = ""

    if type(cmd) == list:
        command = "\\%;".join(cmd)
    else:
        command = cmd

    tf.eval(definition % (mType, alias, command))
