from direct.fsm.FSM import FSM


# Game State Class
# ================
class GameState(FSM):
    def request(self, request, *args):
        # Store previous state before transitioning
        self.prev_state = self.state
        return FSM.request(self, request, *args)

    def enterSplashScreen(self):
        # Show splash screen and play title screen music
        base.ui.switch_to_screen("SplashScreen")  # noqa: F821
        base.title_music.play()  # noqa: F821

    def exitSplashScreen(self):
        # Enable pause menu
        base.accept("escape", base.toggle_pause)  # noqa: F821

    def enterTitleScreen(self):
        # Show title screen
        base.ui.switch_to_screen("TitleScreen")  # noqa: F821

    def exitTitleScreen(self):
        pass

    def enterCampaignScreen(self):
        # Show campaign screen
        base.ui.switch_to_screen("CampaignScreen")  # noqa: F821

    def exitCampaignScreen(self):
        pass

    def enterLoginScreen(self):
        # Show the login screen
        base.ui.switch_to_screen("LoginScreen")  # noqa: F821

    def exitLoginScreen(self):
        pass

    def enterConnectingScreen(self, username, password):
        # Show the connecting screen
        base.ui.switch_to_screen("LoadingScreen")  # noqa: F821

        # Do login
        print("Connecting...")
        print(f"username = {username}")
        print(f"password = {password}")

    def exitConnectingScreen(self):
        pass

    def enterCharacterSelectScreen(self):
        # Show the character select screen
        base.ui.switch_to_screen("CharacterSelectScreen")  # noqa: F821

    def exitCharacterSelectScreen(self):
        pass

    def enterCharacterEditorScreen(self):
        # Show the character editor screen
        base.ui.switch_to_screen("CharacterEditorScreen")  # noqa: F821

    def exitCharacterEditorScreen(self):
        pass

    def enterGame(self, mode="ResumeGame"):
        # Show the ingame HUD
        base.ui.switch_to_screen("HUD")  # noqa: F821
        print(f"Game Mode: {mode}")

    def exitGame(self):
        pass

    def enterPause(self):
        # Show pause menu
        base.ui.switch_to_screen("PauseMenu")  # noqa: F821

    def exitPause(self):
        pass

    def enterSettingsScreen(self):
        # Show settings screen
        base.ui.switch_to_screen("Settings")  # noqa: F821

    def exitSettingsScreen(self):
        pass
