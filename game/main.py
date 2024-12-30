from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    load_prc_file
)


# Application Class
# =================
class NeoImpressiveTitle(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("config.prc")

        # Call base constructor
        ShowBase.__init__(self)


# Entry Point
# ===========
if __name__ == "__main__":
    NeoImpressiveTitle().run()
