class AudioManager(object):
    def __init__(self):
        # Load title screen music
        self.title_music = base.loader.load_music("music/Title.ogg")
        self.title_music.set_loop(True)

        # Load sound effects
        self.click_sfx = base.loader.load_sfx("sfx/Click.ogg")

    def play_title_screen_music(self, state):
        # Play or stop the music
        if state:
            self.title_music.play()

        else:
            self.title_music.stop()

    def play_click_sfx(self):
        self.click_sfx.play()
