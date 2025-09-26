from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import (
    load_prc_file
)

from ui.neoimpressivetitleui import NeoImpressiveTitleUI
from game_state import GameState


# Application Class
# =================
class NeoImpressiveTitle(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("settings.prc")

        # Call base constructor
        ShowBase.__init__(self)

        # Initialize UI
        self.ui = NeoImpressiveTitleUI(self)
        self.ui.run()

        # Load music
        self.title_music = self.loader.load_music("music/Title.ogg")
        self.title_music.set_loop(True)

        # Load sound effects
        self.click_sfx = self.loader.load_sfx("sfx/Click.ogg")

        # Schedule game initialization
        self.task_mgr.add(self.init_game(), "init")

    async def init_game(self):
        # Yield first timeslice to ensure full UI initialization
        await Task.pause(0)

        # Initialize game state
        self.game_state = GameState("GameState")
        self.game_state.request("SplashScreen")
        self.game_state.request("Pause")

    def toggle_pause(self):
        if self.game_state.state != "Pause":
            self.game_state.request("Pause")

        else:
            self.game_state.request(self.game_state.prev_state)

    def exit_game(self, task):
        # Exit the game
        self.userExit()
        return task.done


# Entry Point
# ===========
if __name__ == "__main__":
    NeoImpressiveTitle().run()
