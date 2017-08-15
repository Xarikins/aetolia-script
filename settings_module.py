from core.module import Module
import state
import json
import os

class Settings(Module):

    DEFAULT_SETTINGS =  {
            "afflictions_file": "afflictions.json",
            "defences_file": "defences.json",
            "map_file": "map.xml",
            "map_url": "http://www.aetolia.com/maps/map.xml",
            "affliction_list_file": "afflictions.list",
            "paths": {
                "path_dir": "paths",
                },
            "notifications": {
                "icon_file": "aet_notify_icon.png",
                },
            }

    def __init__(self, *args):
        super(Settings, self).__init__(*args)

        self.state["alias_builder"].build({
            "settings show": self.render_settings,
            })
        self.load_settings()

    def load_settings(self):
        filename = "settings.json"
        if os.path.isfile(filename):
            self.mud.info("Loading settings from: %s" % filename)
            with open(filename) as f:
                self.state["settings"] = json.loads(f.read())
        else:
            self.mud.info("Loading default settings")
            self.state["settings"] = self.DEFAULT_SETTINGS
        self.mud.out("%s" % os.getcwd())
        
    def get_setting(self, key):
        return self.state["settings"][key]

    def get_path_filename_for(self, name):
        return "%s/%s.json" % (self.state["settings"]["paths"]["path_dir"], name)

    def render_settings(self):
        self.mud.panic("SETTINGS:")
        self.__print_dict(self.state["settings"])

    def __print_dict(self, data, indent=""):
        for key, setting in data.items():
            if type(setting) == dict:
                self.mud.echop("@{Cgreen}%s%s@{n}: (" % (indent, key))
                self.__print_dict(setting, "    ")
                self.mud.out("%s)" % indent)
            else:
                self.mud.echop("@{Cgreen}%s%s@{n}: @{Cred}%s@{n}" % (indent, key, str(setting)))

if __name__ == "__main__":
    cstate = state.new()
    settings = Settings(cstate)
    settings.render_settings()
