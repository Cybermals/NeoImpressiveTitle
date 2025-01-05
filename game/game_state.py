from direct.fsm.FSM import FSM


# Game State Class
# ================
class GameState(FSM):
    def enterSplashScreen(self):
        # Show splash screen and play title screen music
        base.ui.switch_to_screen("SplashScreen")
        base.title_music.play()

    def exitSplashScreen(self):
        pass

    def enterTitleScreen(self):
        # Show title screen
        base.ui.switch_to_screen("TitleScreen")

    def exitTitleScreen(self):
        pass
