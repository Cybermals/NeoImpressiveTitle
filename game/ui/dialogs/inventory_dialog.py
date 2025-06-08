from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.bubble import Bubble

from ui.theme import GameFloatingWindow

import ui.item_list  # noqa: F401


# Classes
# =======
class ItemBubble(Bubble):
    item = ObjectProperty()

    def on_touch_up(self, touch):
        # Call base method
        super().on_touch_up(touch)

        # Was the click inside the bubble?
        if self.collide_point(touch.x, touch.y):
            return True

        # Close the bubble
        self.parent.remove_widget(self)
        return False


class InventoryDialog(GameFloatingWindow):
    equipped_items = ObjectProperty()

    def on_touch_down(self, touch):
        self.mouse_pos = touch.pos
        return super().on_touch_down(touch)

    def on_equipped_items(self, instance, value):
        # Display test data
        self.equipped_items.data = [{
            "text": f"Item {i + 1}",
            "command": lambda item: self.show_item_menu(item)
            } for i in range(100)]

    def show_item_menu(self, item):
        # Create item bubble if it doesn't exist
        if not hasattr(self, "item_bubble"):
            self.item_bubble = ItemBubble()

        # Set selected item and bubble position
        self.item_bubble.item = item
        self.item_bubble.center_x = self.mouse_pos[0]
        self.item_bubble.y = self.mouse_pos[1]

        # Show item bubble
        if self.item_bubble.parent is None:
            self.add_widget(self.item_bubble)

    def stash_item(self, item):
        print(f"Stash '{item.text}'")
        self.remove_widget(self.item_bubble)

    def drop_item(self, item):
        print(f"Drop '{item.text}'")
        self.remove_widget(self.item_bubble)

    def delete_item(self, item):
        print(f"Delete '{item.text}'")
        self.remove_widget(self.item_bubble)


Builder.load_file("ui/dialogs/inventory_dialog.kv")
