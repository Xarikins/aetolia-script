from imp import reload
import prompt
import combat
import info_here_parser
import affliction_parser
import curing_module

def build_modules(state):
    reload(prompt)
    reload(combat)
    reload(info_here_parser)
    reload(affliction_parser)

    combat_mod = combat.CombatModule(state)

    modules = []
    modules.append(prompt.PromptParser(state))
    modules.append(combat_mod)
    modules.append(info_here_parser.InfoParser(combat_mod, state))
    modules.append(curing_module.CuringModule(state))
    #modules.append(affliction_parser.AfflictionParser(state))
    return modules
