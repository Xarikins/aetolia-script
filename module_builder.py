from imp import reload
import prompt
import combat_module
import hilite_module
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
import path_queue_module
import refining_module
import settings_module

def build_modules(state):
    reload(prompt)
    reload(combat_module)
    reload(hilite_module)
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
    reload(path_queue_module)
    reload(refining_module)
    reload(settings_module)

    modules = []
    modules.append(settings_module.Settings(state)) # Needs to be first
    modules.append(prompt.PromptParser(state))
    modules.append(combat_module.CombatModule(state))
    modules.append(hilite_module.HiliteModule(state))
    modules.append(info_here_parser.InfoParser(state))
    modules.append(curing_module.CuringModule(state))
    modules.append(notification_module.NotificationModule(state))
    modules.append(map_module.MapModule(state))
    modules.append(hunting_module.HuntingModule(state))
    modules.append(movement_module.MovementModule(state))
    modules.append(harvest_module.HarvestModule(state))
    modules.append(mount_module.MountModule(state))
    modules.append(gmcp_module.GmcpModule(state))
    modules.append(statusbar_module.StatusBarModule(state))
    modules.append(aff_tracker_module.AffTrackerModule(state))
    modules.append(target_skills_module.TargetSkillsModule(state))
    modules.append(combat_attacks_module.CombatAttacksModule(state))
    modules.append(composer_module.ComposerModule(state))
    modules.append(wield_module.WieldModule(state))
    modules.append(queue_module.QueueModule(state))
    modules.append(path_queue_module.PathQueueModule(state))
    modules.append(refining_module.RefiningModule(state))
    #modules.append(affliction_parser.AfflictionParser(state))

    return modules
