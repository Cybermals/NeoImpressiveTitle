from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    load_prc_file
)

from ui import NeoImpressiveTitleUI
from game_state import GameState


# Application Class
# =================
class NeoImpressiveTitle(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("config.prc")

        # Call base constructor
        ShowBase.__init__(self)

        # Initialize UI
        self.ui = NeoImpressiveTitleUI(self)
        self.ui.run()

        # Load music
        self.title_music = self.loader.load_music("music/Title.ogg")
        self.title_music.set_loop(True)

        # Initialize game state
        self.game_state = GameState("GameState")
        self.game_state.request("SplashScreen")


# Entry Point
# ===========
if __name__ == "__main__":
    NeoImpressiveTitle().run()
