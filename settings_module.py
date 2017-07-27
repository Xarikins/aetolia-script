from core.module import Module

class SettingsModule(Module):

    def __init__(self, *args):
        super(SettingsModule, self).__init__(*args)
        
        self.__load_settings()

    def __load_settings():
        pass
        
