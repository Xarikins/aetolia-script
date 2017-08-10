from imp import reload
import prompt
import combat
import combat_hilite_module
import info_here_parser
import affliction_parser
import curing_module
import notification_module
import map_module
import hunting_module
import movement_module
import harvest_module
import mount_module
import gmcp_module
import statusbar_module
import queue_module
import aff_tracker_module
import target_skills_module
import combat_attacks_module
import composer_module
import wield_module

def build_modules(state):
    reload(prompt)
    reload(combat)
    reload(combat_hilite_module)
    reload(info_here_parser)
    reload(affliction_parser)
    reload(notification_module)
    reload(map_module)
    reload(hunting_module)
    reload(movement_module)
    reload(harvest_module)
    reload(gmcp_module)
    reload(mount_module)
    reload(statusbar_module)
    reload(queue_module)
    reload(aff_tracker_module)
    reload(target_skills_module)
    reload(combat_attacks_module)
    reload(composer_module)
    reload(wield_module)

    combat_mod = combat.CombatModule(state)
    hunting_mod = hunting_module.HuntingModule(state)

    modules = []
    modules.append(prompt.PromptParser(state))
    modules.append(combat_mod)
    modules.append(combat_hilite_module.CombatHiliteModule(state))
    modules.append(info_here_parser.InfoParser(combat_mod, hunting_mod, state))
    modules.append(curing_module.CuringModule(state))
    modules.append(notification_module.NotificationModule(state))
    modules.append(map_module.MapModule(state))
    modules.append(hunting_mod)
    modules.append(movement_module.MovementModule(state))
    modules.append(harvest_module.HarvestModule(state))
    modules.append(mount_module.MountModule(state))
    modules.append(gmcp_module.GmcpModule(state))
    modules.append(statusbar_module.StatusBarModule(state))
    modules.append(queue_module.QueueModule(state))
    modules.append(aff_tracker_module.AffTrackerModule(state))
    modules.append(target_skills_module.TargetSkillsModule(state))
    modules.append(combat_attacks_module.CombatAttacksModule(state))
    modules.append(composer_module.ComposerModule(state))
    modules.append(wield_module.WieldModule(state))
    #modules.append(affliction_parser.AfflictionParser(state))
    return modules
