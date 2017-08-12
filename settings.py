from core.module import Module

class Settings(Module):

    def __init__(self, *args):
        super(Settings, self).__init__(*args)

        self.settings =  {
                }

    def load_settings(self):
        pass
        
    def save_settings(self):
        pass

    def render_settings(self):
        pass
