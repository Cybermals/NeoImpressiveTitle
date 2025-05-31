from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition


# Classes
# =======
class TargetHPPanel(ScreenManager):
    def show(self):
        self.transition = SlideTransition(direction="down")
        self.current = "Visible"
    
    def hide(self):
        self.transition = SlideTransition(direction="up")
        self.current = "Hidden"


Builder.load_file("ui/target_hp_panel.kv")
