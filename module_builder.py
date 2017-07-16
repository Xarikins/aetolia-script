from imp import reload
import prompt
import combat
import info_here_parser
import affliction_parser
import curing_module
import notification_module
import map_module
import hunting_module

def build_modules(state):
    reload(prompt)
    reload(combat)
    reload(info_here_parser)
    reload(affliction_parser)
    reload(notification_module)
    reload(map_module)
    reload(hunting_module)

    combat_mod = combat.CombatModule(state)

    modules = []
    modules.append(prompt.PromptParser(state))
    modules.append(combat_mod)
    modules.append(info_here_parser.InfoParser(combat_mod, state))
    modules.append(curing_module.CuringModule(state))
    modules.append(notification_module.NotificationModule(state))
    modules.append(map_module.MapModule(state))
    modules.append(hunting_module.HuntingModule(state))
    #modules.append(affliction_parser.AfflictionParser(state))
    return modules
