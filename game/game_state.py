from direct.fsm.FSM import FSM


# Game State Class
# ================
class GameState(FSM):
    def enterSplashScreen(self):
        # Play title screen music
        base.title_music.play()

    def exitSplashScreen(self):
        pass
